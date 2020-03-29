# TODO : setup rabbit listeners; "update_es": [informationmodels,concepts,datasets,dataservices]
import json
import math
import time

import requests
import os
from elasticsearch import Elasticsearch, helpers
from .utils import Indexes
from jsonpath_ng import parse

ES_HOST = os.getenv('ELASTIC_HOST') or "localhost"
ES_PORT = os.getenv('ELASTIC_PORT') or "9200"
client = Elasticsearch([ES_HOST + ':' + ES_PORT])
API_URL = os.getenv('API_URL')


def fetch_from_services():
    start = time.time()
    info_status = fetch_information_models()
    concept_status = fetch_concepts()
    service_status = fetch_dataservices()
    datasets_status = fetch_datasets()
    total_time = time.time() - start
    total_concepts = 0
    for iteration in concept_status:
        total_concepts = total_concepts + iteration[0]
    totalElements = info_status[0]+total_concepts+service_status[0]+datasets_status[0]
    result = {
        "took": total_time,
        "total": totalElements,
        "informationmodels": info_status,
        "concepts": concept_status,
        "dataservice": service_status,
        "datasets": datasets_status
    }
    return result


def fetch_information_models():
    print("fetching information models")
    info_url = API_URL + "informationmodels"
    size = requests.request(url=info_url, method="GET")
    totalElements = size.json()["page"]["totalElements"]
    r = requests.request(url=info_url + "?size=" + str(totalElements), method="GET")
    documents = r.json()["_embedded"]["informationmodels"]
    result = elasticsearch_ingest(documents, Indexes.INFO_MODEL, Indexes.INFO_MODEL_ID_KEY)
    return result


def fetch_concepts():
    print("fetching concepts")
    concept_url = API_URL + "concepts"
    size = requests.request(url=concept_url, method="GET")
    totalElements = size.json()["page"]["totalElements"]
    doRequest = math.ceil(totalElements / 1000)
    # repeat request if totalElements exceeds max size of response
    if doRequest > 1:
        results = []
        for x in range(doRequest):
            r = requests.request(url=concept_url + "?size=1000&page=" + str(x), method="GET")
            documents = r.json()["_embedded"]["concepts"]
            result = elasticsearch_ingest(documents, Indexes.CONCEPTS, Indexes.CONCEPTS_ID_KEY)
            results.append(result)
        return results
    else:
        r = requests.request(url=concept_url + "?size" + str(totalElements), method="GET")
        documents = r.json()["_embedded"]["concepts"]
        result = elasticsearch_ingest(documents, Indexes.CONCEPTS, Indexes.CONCEPTS_ID_KEY)
        return result


def fetch_datasets():
    print("fetching datasets")
    dataset_url = API_URL + "datasets"
    size = requests.get(url=dataset_url, headers={"Accept": "application/json"}).json()["hits"]["total"]
    r = requests.get(url=dataset_url + "?size=" + str(size), headers={"Accept": "application/json"})
    documents = r.json()["hits"]["hits"]
    doRequest = math.ceil(size / len(documents))
    if doRequest > 1:
        for x in range(1, doRequest):
            r = requests.get(url=dataset_url + "?size=100" + "&page=" + str(x), headers={"Accept": "application/json"})
            documents = documents + r.json()["hits"]["hits"]
    result = elasticsearch_ingest_from_source(documents, Indexes.DATA_SETS, Indexes.DATA_SETS_ID_KEY)
    return result


def fetch_dataservices():
    print("fetching services")
    data_service_url = API_URL + "apis"
    size = requests.get(url=data_service_url, headers={"Accept": "application/json"}).json()["total"]
    r = requests.get(url=data_service_url + "?size=" + str(size), headers={"Accept": "application/json"})
    documents = r.json()
    id_path = parse('hits[*].id')
    id_list = [match.value for match in id_path.find(documents)]
    # repeat request if size exceeds max size of response
    if len(id_list) < size:
        doRequest = math.ceil(size / 100)
        for x in range(1, doRequest):
            r = requests.request(url=data_service_url + "?size=100&page=" + str(x), method="GET")
            id_list = id_list + [match.value for match in id_path.find(r.json())]
    hits = []
    # get full documents
    for api_id in id_list:
        r = requests.get(url=data_service_url + "/" + api_id, headers={"Accept": "application/json"})
        doc = r.json()
        hits.append(doc)

    result = elasticsearch_ingest(hits, "dataservices", "id")
    return result


def elasticsearch_ingest(documents, index, id_key):
    result = helpers.bulk(client=client, actions=yield_documents(documents, index, id_key))
    return result


def elasticsearch_ingest_from_source(documents, index, id_key):
    result = helpers.bulk(client=client, actions=yield_documents_from_source(documents, index, id_key))
    return result


def yield_documents(documents, index, id_key):
    for doc in documents:
        yield {
            "_index": index,
            "_id": doc[id_key],
            "_source": doc
        }


def yield_documents_from_source(documents, index, id_key):
    for doc in documents:
        yield {
            "_index": index,
            "_id": doc["_id"],
            "_source": doc["_source"]
        }


def create_indices():
    with open(os.getcwd() + "/elasticsearch/create_concept_index.json") as concept_mapping:
        try:
            client.indices.delete(index="concepts")
        except:
            print("indices concept does not exist")
        finally:
            client.indices.create(index="concepts", body=json.load(concept_mapping))
    with open(os.getcwd() + "/elasticsearch/create_dataservices_index.json") as dataservice_mapping:
        try:
            client.indices.delete(index="dataservices")
        except:
            print("indices dataservices does not exist")
        finally:
            client.indices.create(index="dataservices", body=json.load(dataservice_mapping))
    with open(os.getcwd() + "/elasticsearch/create_datasets_index.json") as datasets_mapping:
        try:
            client.indices.delete(index="datasets")
        except:
            print("indices datasets does not exist")
        finally:
            client.indices.create(index="datasets", body=json.load(datasets_mapping))
    with(open(os.getcwd() + "/elasticsearch/create_info_index.json")) as info_mapping:
        try:
            client.indices.delete(index="informationmodels")
        except:
            print("indices informationmodels does not exist")
        finally:
            client.indices.create(index="informationmodels", body=json.load(info_mapping))
