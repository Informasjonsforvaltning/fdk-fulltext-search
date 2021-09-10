from dataclasses import asdict
from datetime import datetime
import json
from json import JSONDecodeError
import logging
import os
import time
import traceback
from typing import Any, Dict, Generator, Optional, Union

from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import BulkIndexError
import fdk_rdf_parser
import requests
from requests import HTTPError, RequestException, Timeout
import simplejson

from .utils import IndicesKey, PipelinesKey

ES_HOST = os.getenv("ELASTIC_HOST", "localhost")
ES_PORT = os.getenv("ELASTIC_PORT", "9200")
es_client = Elasticsearch([ES_HOST + ":" + ES_PORT])
API_URL = os.getenv("API_URL", "http://localhost:8080/")
DATASET_HARVESTER_BASE_URI = os.getenv(
    "DATASET_HARVESTER_BASE_URI", "http://localhost:8080/dataset"
)
FDK_DATASERVICE_HARVESTER_URI = os.getenv(
    "FDK_DATASERVICE_HARVESTER_URI", "http://localhost:8080/dataservice"
)
FDK_SERVICE_HARVESTER_URI = os.getenv(
    "FDK_SERVICE_HARVESTER_URI", "http://localhost:8080"
)
FDK_EVENT_HARVESTER_URI = os.getenv("FDK_EVENT_HARVESTER_URI", "http://localhost:8080")
MODEL_HARVESTER_URI = os.getenv(
    "MODEL_HARVESTER_URI", "http://localhost:8080/infomodel"
)
FDK_CONCEPT_HARVESTER_URI = os.getenv(
    "FDK_CONCEPT_HARVESTER_URI", "http://localhost:8080/concept"
)

RECORDS_PARAM_TRUE = {"catalogrecords": "true"}


def error_msg(
    exec_point: str, reason: Union[str, BaseException], count: int = 0
) -> Dict[str, Union[str, int]]:
    return {
        "count": count,
        "status": "error",
        "message": f"Exception when attempting to {exec_point}: \n: {reason}",
    }


def result_msg(count: int) -> Dict[str, Union[str, int]]:
    return {"status": "OK", "count": count}


def reindex() -> Dict:
    result = fetch_all_content()
    return result


def fetch_all_content() -> Dict:
    start = time.time()
    info_status = fetch_information_models()
    concept_status = fetch_concepts()
    service_status = fetch_data_services()
    datasets_status = fetch_data_sets()
    public_services_status = fetch_public_services()
    events_status = fetch_events()
    total_time = time.time() - start
    total_elements = (
        int(info_status["count"])
        + int(concept_status["count"])
        + int(service_status["count"])
        + int(datasets_status["count"])
        + int(public_services_status["count"])
    )
    status = "erros occured"
    if (
        info_status["status"] == "OK"
        and concept_status["status"] == "OK"
        and service_status["status"] == "OK"
        and datasets_status["status"] == "OK"
        and public_services_status["status"] == "OK"
        and events_status["status"] == "OK"
    ):
        status = "OK"
    result = {
        "status": status,
        "took": total_time,
        "total": total_elements,
        "informationmodels": info_status,
        "concepts": concept_status,
        "dataservice": service_status,
        "datasets": datasets_status,
        "public_services": public_services_status,
        "events": events_status,
    }
    logging.info("update of all services completed\n {}".format(result))
    return result


def fetch_information_models() -> Dict[str, Union[str, int]]:
    info_url = f"{MODEL_HARVESTER_URI}/catalogs"

    logging.info(f"fetching information models from {info_url}")
    try:
        response = requests.get(
            url=info_url,
            params=RECORDS_PARAM_TRUE,
            headers={"Accept": "text/turtle"},
            timeout=10,
        )
        response.raise_for_status()

        parsed_rdf = fdk_rdf_parser.parse_information_models(response.text)
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.INFO_MODEL}-{os.urandom(4).hex()}"

            create_error = create_index(IndicesKey.INFO_MODEL, new_index_name)
            if create_error:
                return create_error

            logging.info("ingesting parsed information models")
            result = elasticsearch_ingest_from_harvester(
                parsed_rdf, new_index_name, IndicesKey.INFO_MODEL_ID_KEY
            )

            alias_error = set_alias_for_new_index(IndicesKey.INFO_MODEL, new_index_name)
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            try:
                raise Exception("could not parse data services")
            except Exception:
                logging.error(traceback.format_exc())
            return error_msg(
                f"fetch information models from {info_url} ",
                "could not parse data services",
            )
    except Exception as err:
        result = error_msg(f"fetch information models from {info_url} ", err)
        logging.error(f"{traceback.format_exc()} {result['message']}")
        return result


def fetch_concepts() -> Dict[str, Union[str, int]]:
    concept_url = f"{FDK_CONCEPT_HARVESTER_URI}/collections"
    logging.info(f"fetching concepts from {concept_url}")
    try:
        response = requests.get(
            url=concept_url,
            params=RECORDS_PARAM_TRUE,
            headers={"Accept": "text/turtle"},
            timeout=10,
        )
        response.raise_for_status()

        parsed_rdf = fdk_rdf_parser.parse_concepts(response.text)
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.CONCEPTS}-{os.urandom(4).hex()}"

            create_error = create_index(IndicesKey.CONCEPTS, new_index_name)
            if create_error:
                return create_error

            logging.info("ingesting parsed concepts")
            result = elasticsearch_ingest_from_harvester(
                parsed_rdf, new_index_name, IndicesKey.CONCEPTS_ID_KEY
            )

            alias_error = set_alias_for_new_index(IndicesKey.CONCEPTS, new_index_name)
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            try:
                raise Exception("could not parse concepts")
            except Exception:
                logging.error(traceback.format_exc())
            return error_msg(
                f"fetch concepts from {concept_url}", "could not parse concepts"
            )
    except Exception as err:
        result = error_msg(f"fetch concepts from {concept_url}", err)
        logging.error(f"{traceback.format_exc()} {result['message']}")
        return result


def fetch_data_sets() -> Dict[str, Union[str, int]]:
    dataset_url = DATASET_HARVESTER_BASE_URI + "/catalogs"
    try:
        logging.info("fetching datasets")
        req = requests.get(
            url=dataset_url,
            params=RECORDS_PARAM_TRUE,
            headers={"Accept": "text/turtle"},
            timeout=30,
        )
        req.raise_for_status()
        parsed_rdf = fdk_rdf_parser.parse_datasets(req.text)
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.DATA_SETS}-{os.urandom(4).hex()}"

            create_or_update_dataset_pipeline(PipelinesKey.DATA_SETS)
            create_error = create_index(IndicesKey.DATA_SETS, new_index_name)
            if create_error:
                return create_error

            logging.info("ingesting parsed datasets")
            result = elasticsearch_ingest_from_harvester(
                parsed_rdf,
                new_index_name,
                IndicesKey.DATA_SETS_ID_KEY,
                PipelinesKey.DATA_SETS,
            )

            alias_error = set_alias_for_new_index(IndicesKey.DATA_SETS, new_index_name)
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            try:
                raise Exception("could not parse datasets")
            except Exception:
                logging.error(traceback.format_exc())
            return error_msg(
                f"fetch datasets from {dataset_url}", "could not parse datasets"
            )
    except (HTTPError, RequestException, JSONDecodeError, Timeout, KeyError) as err:
        result = error_msg(f"fetch datasets from {dataset_url}", err)
        logging.error(f"{traceback.format_exc()} {result['message']}")
        return result


def fetch_data_services() -> Dict[str, Union[str, int]]:
    dataservice_url = f"{FDK_DATASERVICE_HARVESTER_URI}/catalogs"

    logging.info(f"fetching data services from {dataservice_url}")
    try:
        response = requests.get(
            url=dataservice_url,
            params=RECORDS_PARAM_TRUE,
            headers={"Accept": "text/turtle"},
            timeout=10,
        )
        response.raise_for_status()

        parsed_rdf = fdk_rdf_parser.parse_data_services(response.text)
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.DATA_SERVICES}-{os.urandom(4).hex()}"

            create_or_update_dataservice_pipeline(PipelinesKey.DATA_SERVICES)
            create_error = create_index(IndicesKey.DATA_SERVICES, new_index_name)
            if create_error:
                return create_error

            logging.info("ingesting parsed data services")
            result = elasticsearch_ingest_from_harvester(
                parsed_rdf,
                new_index_name,
                IndicesKey.DATA_SERVICES_ID_KEY,
                PipelinesKey.DATA_SERVICES,
            )

            alias_error = set_alias_for_new_index(
                IndicesKey.DATA_SERVICES, new_index_name
            )
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            try:
                raise Exception("could not parse data services")
            except Exception:
                logging.error(traceback.format_exc())
            return error_msg(
                f"fetch dataservices from {dataservice_url}",
                "could not parse data services",
            )
    except Exception as err:
        result = error_msg(f"fetch dataservices from {dataservice_url}", err)
        logging.error(f"{traceback.format_exc()} {result['message']}")
        return result


def fetch_public_services() -> Dict[str, Union[str, int]]:
    event_url = f"{FDK_EVENT_HARVESTER_URI}/events"
    event_response = None
    try:
        event_response = requests.get(
            url=event_url,
            params=RECORDS_PARAM_TRUE,
            headers={"Accept": "text/turtle"},
            timeout=10,
        )
        event_response.raise_for_status()
    except Exception as err:
        event_result = error_msg(f"fetch events from {event_url}", err)
        logging.error(f"{traceback.format_exc()} {event_result['message']}")

    public_service_url = f"{FDK_SERVICE_HARVESTER_URI}/public-services"

    logging.info(f"fetching public_services from {public_service_url}")
    try:
        response = requests.get(
            url=public_service_url,
            params=RECORDS_PARAM_TRUE,
            headers={"Accept": "text/turtle"},
            timeout=10,
        )
        response.raise_for_status()

        parsed_rdf = fdk_rdf_parser.parse_public_services(
            response.text, event_response.text if event_response is not None else None
        )
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.PUBLIC_SERVICES}-{os.urandom(4).hex()}"

            create_error = create_index(IndicesKey.PUBLIC_SERVICES, new_index_name)
            if create_error:
                return create_error

            logging.info("ingesting parsed public_services")
            result = elasticsearch_ingest_from_harvester(
                parsed_rdf, new_index_name, IndicesKey.PUBLIC_SERVICES_ID_KEY
            )

            alias_error = set_alias_for_new_index(
                IndicesKey.PUBLIC_SERVICES, new_index_name
            )
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            try:
                raise Exception("could not parse public_services")
            except Exception:
                logging.error(traceback.format_exc())
            return error_msg(
                f"fetch public_services from {public_service_url}",
                "could not parse public_services",
            )
    except Exception as err:
        result = error_msg(f"fetch public_services from {public_service_url}", err)
        logging.error(f"{traceback.format_exc()} {result['message']}")
        return result


def fetch_events() -> Dict[str, Union[str, int]]:
    event_url = f"{FDK_EVENT_HARVESTER_URI}/events"

    logging.info(f"fetching events from {event_url}")
    try:
        response = requests.get(
            url=event_url,
            params=RECORDS_PARAM_TRUE,
            headers={"Accept": "text/turtle"},
            timeout=10,
        )
        response.raise_for_status()

        parsed_rdf = fdk_rdf_parser.parse_events(response.text)
        if parsed_rdf is not None:
            new_index_name = f"{IndicesKey.EVENTS}-{os.urandom(4).hex()}"

            create_error = create_index(IndicesKey.EVENTS, new_index_name)
            if create_error:
                return create_error

            logging.info("ingesting parsed public_services")
            result = elasticsearch_ingest_from_harvester(
                parsed_rdf, new_index_name, IndicesKey.EVENTS_ID_KEY
            )

            alias_error = set_alias_for_new_index(IndicesKey.EVENTS, new_index_name)
            if alias_error:
                return alias_error

            return result_msg(result[0])
        else:
            try:
                raise Exception("could not parse events")
            except Exception:
                logging.error(traceback.format_exc())
            return error_msg(f"fetch events from {event_url}", "could not parse events")
    except Exception as err:
        result = error_msg(f"fetch events from {event_url}", err)
        logging.error(f"{traceback.format_exc()} {result['message']}")
        return result


def elasticsearch_ingest_from_harvester(
    documents: Any, index: str, id_key: str, pipeline: str = None
) -> Any:
    try:
        result = helpers.bulk(
            client=es_client,
            actions=yield_documents_from_harvester(documents, index, id_key, pipeline),
        )

        return result
    except BulkIndexError as err:
        result = error_msg(f"ingest {index}", err.errors)
        logging.error(f"{traceback.format_exc()} {result['message']}")
        return result


def yield_documents_from_harvester(
    documents: Any, index: str, id_key: str, pipeline: str = None
) -> Generator:
    """get docs from harvester responses"""
    for doc_index in documents:
        doc = {
            "_index": index,
            "_id": documents[doc_index].id,
            "_source": simplejson.dumps(
                asdict(documents[doc_index]), iterable_as_array=True
            ),
        }

        if pipeline:
            doc["pipeline"] = pipeline

        yield doc


def create_index(
    index_alias: str, new_index_name: str
) -> Optional[Dict[str, Union[str, int]]]:
    """create an index with settings and mapping from file"""
    logging.info(f"creating {new_index_name}")
    with open(
        f"{os.getcwd()}/elasticsearch/create_{index_alias}_index.json"
    ) as mapping:
        try:
            es_client.indices.create(index=new_index_name, body=json.load(mapping))

            if not es_client.indices.exists(index=new_index_name):
                return error_msg(
                    f"create index '{new_index_name}'",
                    f"index '{new_index_name}' not created",
                )

            update_index_info(index_alias)
        except BaseException as err:
            logging.error(
                f"{traceback.format_exc()}: error when attempting to create {new_index_name}"
            )
            return error_msg(f"create index '{new_index_name}'", err)
        return None


def set_alias_for_new_index(
    index_alias: str, new_index_name: str
) -> Optional[Dict[str, Union[str, int]]]:
    """Delete old index and set alias for new index"""
    logging.info(f"set alias {index_alias} for index {new_index_name}")
    try:
        if es_client.indices.exists_alias(name=index_alias):
            alias_indices_dict = es_client.indices.get(index=index_alias)
            for index_name in alias_indices_dict:
                es_client.indices.delete(index=index_name)

        es_client.indices.put_alias(index=new_index_name, name=index_alias)
        # TODO add public_services to SEARCHABLE_ALIAS when ready to search in index
        if index_alias not in [IndicesKey.PUBLIC_SERVICES, IndicesKey.EVENTS]:
            es_client.indices.put_alias(
                index=new_index_name, name=IndicesKey.SEARCHABLE_ALIAS
            )
        if index_alias in [IndicesKey.PUBLIC_SERVICES, IndicesKey.EVENTS]:
            es_client.indices.put_alias(
                index=new_index_name, name=IndicesKey.PUBLIC_SERVICES_AND_EVENTS_ALIAS
            )

    except BaseException as err:
        logging.error(
            f"{traceback.format_exc()}: error when attempting to set alias {index_alias} for index {new_index_name}"
        )
        return error_msg(f"set alias '{index_alias}'", err)
    return None


def update_index_info(index_name: str) -> None:
    now = datetime.now().isoformat()
    if es_client.indices.exists("info"):
        update_query = {
            "query": {"term": {"name": index_name}},
            "script": {"inline": f"ctx._source.lastUpdate='{now}'", "lang": "painless"},
        }
        result = es_client.update_by_query(index="info", body=update_query)
        if result["total"] == 0:
            init_info_doc(index_name, now)
    else:
        init_info_doc(index_name, now)


def init_info_doc(index_name: str, now: str) -> None:
    init_doc = {"name": index_name, "lastUpdate": now}
    if not es_client.indices.exists("info"):
        es_client.indices.create(index="info")
    es_client.index(index="info", body=init_doc)


def create_or_update_dataset_pipeline(pipeline_id: str) -> None:
    try:
        es_client.ingest.get_pipeline(pipeline_id)
        es_client.ingest.delete_pipeline(pipeline_id)
    except NotFoundError:
        pass

    es_client.ingest.put_pipeline(
        pipeline_id,
        {
            "processors": [
                {
                    "script": {
                        "description": "Concatinate fdkFormat type and code",
                        "lang": "painless",
                        "source": """
                        ArrayList formats = new ArrayList();
                        if(ctx['distribution'] != null){
                            for (Map distr : ctx['distribution']) {
                                if(distr['fdkFormat'] != null){
                                    for (Map fmt : distr['fdkFormat']) {
                                        if(fmt['type'] == 'UNKNOWN') {
                                            formats.add('UNKNOWN')
                                        } else {
                                            formats.add(fmt['type'] + ' ' + fmt['name'])
                                        }
                                    }
                                }
                            }
                        }
                        ctx["fdkFormatPrefixed"] = formats
                      """,
                    }
                }
            ]
        },
    )


def create_or_update_dataservice_pipeline(pipeline_id: str) -> None:
    try:
        es_client.ingest.get_pipeline(pipeline_id)
        es_client.ingest.delete_pipeline(pipeline_id)
    except NotFoundError:
        pass

    es_client.ingest.put_pipeline(
        pipeline_id,
        {
            "processors": [
                {
                    "script": {
                        "description": "Concatinate fdkFormat type and code",
                        "lang": "painless",
                        "source": """
                        ArrayList formats = new ArrayList();
                        if(ctx['fdkFormat'] != null){
                            for (Map fmt : ctx['fdkFormat']) {
                                if(fmt['fdkType'] == 'UNKNOWN') {
                                    formats.add('UNKNOWN')
                                } else {
                                    formats.add(fmt['type'] + ' ' + fmt['name'])
                                }
                            }
                        }
                        ctx["fdkFormatPrefixed"] = formats
                      """,
                    }
                }
            ]
        },
    )
