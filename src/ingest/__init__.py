import json
import logging
import math
import time
from datetime import datetime
from dataclasses import asdict
from json import JSONDecodeError

import requests
import os
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
import fdk_rdf_parser
from requests import HTTPError, RequestException, Timeout

from .utils import IndicesKey

ES_HOST = os.getenv('ELASTIC_HOST', 'localhost')
ES_PORT = os.getenv('ELASTIC_PORT', '9200')
es_client = Elasticsearch([ES_HOST + ':' + ES_PORT])
API_URL = os.getenv('API_URL', 'http://localhost:8080/')
DATASET_HARVESTER_BASE_URI = os.getenv('DATASET_HARVESTER_BASE_URI', 'http://localhost:8080/dataset')
FDK_DATASERVICE_HARVESTER_URI = os.getenv('FDK_DATASERVICE_HARVESTER_URI', 'http://localhost:8080/dataservice')


def error_msg(exec_point, reason, count=0):
    return {
        "count": count,
        "status": "error",
        "message": f"Exception when attempting to {exec_point}: \n: {reason}"
    }


def result_msg(count):
    return {
        "status": "OK",
        "count": count
    }


def reindex():
    result = fetch_all_content()
    return result


def fetch_all_content():
    start = time.time()
    info_status = fetch_information_models()
    concept_status = fetch_concepts()
    service_status = fetch_data_services()
    datasets_status = fetch_data_sets()
    total_time = time.time() - start
    totalElements = info_status["count"] + concept_status["count"] + service_status["count"] + datasets_status["count"]
    status = "erros occured"
    if info_status['status'] == 'OK' \
            and concept_status['status'] == 'OK' \
            and service_status['status'] == 'OK' \
            and datasets_status['status'] == 'OK':
        status = "OK"
    result = {
        "status": status,
        "took": total_time,
        "total": totalElements,
        "informationmodels": info_status,
        "concepts": concept_status,
        "dataservice": service_status,
        "datasets": datasets_status
    }
    logging.info("update of all services completed\n {}".format(result))
    return result


def fetch_information_models():
    info_url = API_URL + "informationmodels"
    try:
        logging.info("fetching information models")
        size = requests.get(url=info_url, timeout=5)
        size.raise_for_status()
        totalElements = size.json()["page"]["totalElements"]
        r = requests.get(url=info_url, params={"size": totalElements}, timeout=5)
        r.raise_for_status()

        new_index_name = f"{IndicesKey.INFO_MODEL}-{os.urandom(4).hex()}"

        create_error = create_index(IndicesKey.INFO_MODEL, new_index_name)
        if create_error:
            return create_error

        documents = r.json()["_embedded"]["informationmodels"]
        result = elasticsearch_ingest(documents, new_index_name, IndicesKey.INFO_MODEL_ID_KEY)

        alias_error = set_alias_for_new_index(IndicesKey.INFO_MODEL, new_index_name)
        if alias_error:
            return alias_error

        return result_msg(result[0])
    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch informationmodels from {info_url}", err)
        logging.error(result["message"])
        return result


def fetch_concepts():
    concept_url = API_URL + "concepts"
    try:
        logging.info("fetching concepts")
        size = requests.get(url=concept_url, timeout=5)
        size.raise_for_status()
        totalElements = size.json()["page"]["totalElements"]
        doRequest = math.ceil(totalElements / 1000)
        # repeat request if totalElements exceeds max size of response
        concepts = []
        if doRequest > 1:
            for x in range(doRequest):
                r = requests.get(url=concept_url, params={"size": "1000", "page": str(x)}, timeout=5)
                r.raise_for_status()
                concepts.extend(r.json()["_embedded"]["concepts"])
        else:
            r = requests.get(url=concept_url, params={"size": "1000"}, timeout=5)
            r.raise_for_status()
            concepts = r.json()["_embedded"]["concepts"]

        new_index_name = f"{IndicesKey.CONCEPTS}-{os.urandom(4).hex()}"

        create_error = create_index(IndicesKey.CONCEPTS, new_index_name)
        if create_error:
            return create_error

        result = elasticsearch_ingest(concepts, new_index_name, IndicesKey.CONCEPTS_ID_KEY)

        alias_error = set_alias_for_new_index(IndicesKey.CONCEPTS, new_index_name)
        if alias_error:
            return alias_error

        return result_msg(result[0])

    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch concepts from {concept_url}", err)
        logging.error(result["message"])
        return result


def fetch_data_sets():
    dataset_url = DATASET_HARVESTER_BASE_URI + "/catalogs"
    try:
        logging.info("fetching datasets")
        req = requests.get(url=dataset_url, headers={"Accept": "text/turtle"}, timeout=30)
        req.raise_for_status()
        parsed_rdf = fdk_rdf_parser.parseDatasets(req.text)
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.DATA_SETS}-{os.urandom(4).hex()}"

            create_error = create_index(IndicesKey.DATA_SETS, new_index_name)
            if create_error:
                return create_error

            logging.info(f"ingesting parsed datasets")
            result = elasticsearch_ingest_from_harvester(parsed_rdf, new_index_name, IndicesKey.DATA_SETS_ID_KEY)

            alias_error = set_alias_for_new_index(IndicesKey.DATA_SETS, new_index_name)
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            logging.error("could not parse datasets")
    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch datasets from {dataset_url}", err)
        logging.error(result["message"])
        return result


def fetch_data_services():
    dataservice_url = f'{FDK_DATASERVICE_HARVESTER_URI}/catalogs'

    logging.info(f"fetching data services from {dataservice_url}")
    try:
        response = requests.get(url=dataservice_url, headers={'Accept': 'text/turtle'}, timeout=10)
        response.raise_for_status()

        parsed_rdf = fdk_rdf_parser.parseDataServices(response.text)
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.DATA_SERVICES}-{os.urandom(4).hex()}"

            create_error = create_index(IndicesKey.DATA_SERVICES, new_index_name)
            if create_error:
                return create_error

            logging.info(f"ingesting parsed data services")
            result = elasticsearch_ingest_from_harvester(parsed_rdf, new_index_name, IndicesKey.DATA_SERVICES_ID_KEY)

            alias_error = set_alias_for_new_index(IndicesKey.DATA_SERVICES, new_index_name)
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            logging.error("could not parse data services")
    except Exception as err:
        result = error_msg(f"fetch dataservices from {dataservice_url}", err)
        logging.error(result["message"])
        return result


def elasticsearch_ingest(documents, index, id_key):
    try:
        result = helpers.bulk(client=es_client, actions=yield_documents(documents, index, id_key))
        return result
    except BulkIndexError as err:
        result = error_msg(f"ingest {index}", err.errors)
        logging.error(result)
        return result


def elasticsearch_ingest_from_harvester(documents, index, id_key):
    try:
        result = helpers.bulk(client=es_client, actions=yield_documents_from_harvester(documents, index, id_key))

        return result
    except BulkIndexError as err:
        result = error_msg(f"ingest {index}", err.errors)
        logging.error(result)
        return result


def yield_documents(documents, index, id_key):
    """get docs from responses without ES data"""
    for doc in documents:
        yield {
            "_index": index,
            "_id": doc[id_key],
            "_source": doc
        }


def yield_documents_from_harvester(documents, index, id_key):
    """get docs from harvester responses"""
    for doc_index in documents:
        yield {
            "_index": index,
            "_id": documents[doc_index].id,
            "_source": asdict(documents[doc_index])
        }


def yield_documents_from_source(documents, index, id_key):
    """get docs from responses with ES data"""
    for doc in documents:
        yield {
            "_index": index,
            "_id": doc["_id"],
            "_source": doc["_source"]
        }


def create_index(index_alias, new_index_name):
    """create an index with settings and mapping from file"""
    logging.info(f"creating {new_index_name}")
    with open(f"{os.getcwd()}/elasticsearch/create_{index_alias}_index.json") as mapping:
        try:
            es_client.indices.create(index=new_index_name, body=json.load(mapping))

            if not es_client.indices.exists(index=new_index_name):
                return error_msg(f"create index '{new_index_name}'", f"index '{new_index_name}' not created")

            update_index_info(index_alias)
        except BaseException as err:
            logging.error(f"error when attempting to create {new_index_name}")
            return error_msg(f"create index '{new_index_name}'", err.error)
        return None


def set_alias_for_new_index(index_alias, new_index_name):
    """Delete old index and set alias for new index"""
    logging.info(f"set alias {index_alias} for index {new_index_name}")
    try:
        if es_client.indices.exists_alias(name=index_alias):
            alias_indices_dict = es_client.indices.get(index=index_alias)
            for index_name in alias_indices_dict:
                es_client.indices.delete(index=index_name)

        es_client.indices.put_alias(index=new_index_name, name=index_alias)
        es_client.indices.put_alias(index=new_index_name, name=IndicesKey.SEARCHABLE_ALIAS)
    except BaseException as err:
        logging.error(f"error when attempting to set alias {index_alias} for index {new_index_name}")
        return error_msg(f"set alias '{index_alias}'", err.error)
    return None


def update_index_info(index_name):
    now = datetime.now().isoformat()
    if es_client.indices.exists("info"):
        update_query = {
            "query": {
                "term": {
                    "name": index_name
                }
            },
            "script": {
                "inline": f"ctx._source.lastUpdate='{now}'",
                "lang": "painless"
            }
        }
        result = es_client.update_by_query(index="info", body=update_query)
        if result['total'] == 0:
            init_info_doc(index_name, now)
    else:
        init_info_doc(index_name, now)


def init_info_doc(index_name, now):
    init_doc = {
        "name": index_name,
        "lastUpdate": now
    }
    if not es_client.indices.exists("info"):
        es_client.indices.create(index="info")
    es_client.index(index="info", body=init_doc)
