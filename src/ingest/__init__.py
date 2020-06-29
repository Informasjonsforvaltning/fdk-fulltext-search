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
from jsonpath_ng import parse

ES_HOST = os.getenv('ELASTIC_HOST') or "localhost"
ES_PORT = os.getenv('ELASTIC_PORT') or "9200"
es_client = Elasticsearch([ES_HOST + ':' + ES_PORT])
API_URL = os.getenv('API_URL') or "http://loclahost:8080"
DATASET_HARVESTER_BASE_URI = os.getenv('DATASET_HARVESTER_BASE_URI') or "http://loclahost:8080/dataset"


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
    reindex_all_indices()
    result = fetch_all_content()
    return result


def fetch_all_content(re_index=False):
    start = time.time()
    info_status = fetch_information_models(re_index)
    concept_status = fetch_concepts(re_index)
    service_status = fetch_data_services(re_index)
    datasets_status = fetch_data_sets(re_index)
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


def fetch_information_models(re_index=False):
    info_url = API_URL + "informationmodels"
    try:
        if re_index:
            reindex_error = reindex_specific_index(IndicesKey.INFO_MODEL)
            if reindex_error:
                return reindex_error
        logging.info("fetching information models")
        size = requests.get(url=info_url, timeout=5)
        size.raise_for_status()
        totalElements = size.json()["page"]["totalElements"]
        r = requests.get(url=info_url, params={"size": totalElements}, timeout=5)
        r.raise_for_status()
        documents = r.json()["_embedded"]["informationmodels"]
        result = elasticsearch_ingest(documents, IndicesKey.INFO_MODEL, IndicesKey.INFO_MODEL_ID_KEY)
        return result_msg(result[0])
    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch informationmodels from {info_url}", err)
        logging.error(result["message"])
        return result


def fetch_concepts(re_index=False):
    concept_url = API_URL + "concepts"
    try:
        if re_index:
            reindex_specific_index(IndicesKey.CONCEPTS)
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

        result = elasticsearch_ingest(concepts, IndicesKey.CONCEPTS, IndicesKey.CONCEPTS_ID_KEY)
        return result_msg(result[0])

    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch concepts from {concept_url}", err)
        logging.error(result["message"])
        return result


def fetch_data_sets(re_index=False):
    dataset_url = DATASET_HARVESTER_BASE_URI + "/catalogs"
    try:
        if re_index:
            reindex_specific_index(IndicesKey.DATA_SETS)
        logging.info("fetching datasets")
        req = requests.get(url=dataset_url, headers={"Accept": "text/turtle"}, timeout=10)
        req.raise_for_status()
        documents = fdk_rdf_parser.parseDatasets(req.text)
        result = elasticsearch_ingest_from_harvester(documents, IndicesKey.DATA_SETS, IndicesKey.DATA_SETS_ID_KEY)
        return result_msg(result[0])
    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch datasets from {dataset_url}", err)
        logging.error(result["message"])
        return result


def fetch_data_services(re_index=False):
    logging.info("fetching services")
    data_service_url = API_URL + "apis"
    try:
        if re_index:
            reindex_specific_index(IndicesKey.DATA_SERVICES)
        logging.info("fetching dataseervices")
        size = requests.get(url=data_service_url, headers={"Accept": "application/json"}, timeout=5).json()["total"]
        r = requests.get(url=data_service_url, params={"size": size}, headers={"Accept": "application/json"}, timeout=5)
        r.raise_for_status()
        documents = r.json()
        id_path = parse('hits[*].id')
        id_list = [match.value for match in id_path.find(documents)]
        # repeat request if size exceeds max size of response
        if len(id_list) < size:
            doRequest = math.ceil(size / 100)
            for x in range(1, doRequest):
                r = requests.get(url=data_service_url, params={"size": 100, "page": str(x)}, timeout=5)
                r.raise_for_status()
                id_list = id_list + [match.value for match in id_path.find(r.json())]
        hits = []
        # get full documents
        for api_id in id_list:
            r = requests.get(url=data_service_url + "/" + api_id, headers={"Accept": "application/json"}, timeout=5)
            r.raise_for_status()
            doc = r.json()
            hits.append(doc)

        result = elasticsearch_ingest(hits, IndicesKey.DATA_SERVICES, "id")
        return result_msg(result[0])
    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch dataservices from {data_service_url}", err)
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


def elasticsearch_ingest_from_source(documents, index, id_key):
    try:
        result = helpers.bulk(client=es_client, actions=yield_documents_from_source(documents, index, id_key))

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


def reindex_specific_index(index_name):
    """delete and recreate an index with settings and mapping from file"""
    logging.info("reindexing {0}".format(index_name))
    with open(os.getcwd() + "/elasticsearch/create_{0}_index.json".format(index_name)) as mapping:
        try:
            if es_client.indices.exists(index=index_name):
                es_client.indices.delete(index=index_name)
            es_client.indices.create(index=index_name, body=json.load(mapping))
            update_index_info(index_name)
        except BaseException as err:
            print("error when attempting to update {0} ".format(index_name))
            return error_msg("reindex index '{0}'".format(index_name), err.error)
        return None


def reindex_all_indices():
    with open(os.getcwd() + "/elasticsearch/create_concepts_index.json") as concept_mapping:
        try:
            es_client.indices.delete(index="concepts")
        except:
            print("indices concept does not exist")
        finally:
            es_client.indices.create(index="concepts", body=json.load(concept_mapping))
    with open(os.getcwd() + "/elasticsearch/create_dataservices_index.json") as dataservice_mapping:
        try:
            es_client.indices.delete(index="dataservices")
        except:
            print("indices dataservices does not exist")
        finally:
            es_client.indices.create(index="dataservices", body=json.load(dataservice_mapping))
    with open(os.getcwd() + "/elasticsearch/create_datasets_index.json") as datasets_mapping:
        try:
            es_client.indices.delete(index="datasets")
        except:
            print("indices datasets does not exist")
        finally:
            es_client.indices.create(index="datasets", body=json.load(datasets_mapping))
    with(open(os.getcwd() + "/elasticsearch/create_informationmodels_index.json")) as info_mapping:
        try:
            es_client.indices.delete(index="informationmodels")
        except:
            print("indices informationmodels does not exist")
        finally:
            es_client.indices.create(index="informationmodels", body=json.load(info_mapping))


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
