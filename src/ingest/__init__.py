# TODO : setup rabbit listeners; "new_harvest": [informationmodels,concepts,datasets,dataservices]
import requests
import os
from elasticsearch import Elasticsearch, helpers

ES_HOST = os.getenv('ELASTIC_HOST')
ES_PORT = os.getenv('ELASTIC_PORT')
client = Elasticsearch([ES_HOST+':'+ES_PORT])
API_URL = os.getenv('API_URL')


def fetch_information_models():
    print("fetching information models")
    info_url = API_URL + "informationmodels"
    r = requests.request(url=info_url, method="GET")
    documents = r.json()["_embedded"]["informationmodels"]
    elasticsearch_ingest(documents, "informationmodels")


def fetch_concepts():
    print("fetching concepts")
    concept_url = API_URL + "concepts"
    r = requests.request(url=concept_url, method="GET")
    documents = r.json()["_embedded"]["concepts"]
    elasticsearch_ingest(documents, "concepts")


def fetch_datasets():
    print("fetching datasets")
    dataset_url = API_URL + "datasets"
    r = requests.get(url=dataset_url, headers={"Accept": "application/json"})
    documents = r.json()["hits"]["hits"]
    elasticsearch_ingest(documents, "datasets")


def fetch_dataservices():
    print("fetching services")
    dataserve_url = API_URL + "apis"
    r = requests.get(url=dataserve_url, headers={"Accept": "application/json"})
    documents = r.json()["hits"]
    elasticsearch_ingest(documents, "dataservices")


def elasticsearch_ingest(documents, index):
    result = helpers.bulk(client=client, actions=yield_documents(documents, index))


def elasticsearch_ingest_source(documents, index):
    result = helpers.bulk(client=client, actions=yield_documents_with_source(documents, index))


def yield_documents(documents, index):
    for doc in documents:
        yield {
            "_index": index,
            "_type": "document",
            "doc": doc
        }


def yield_documents_with_source(documents, index):
    for doc in documents:
        yield {
            "_index": index,
            "_type": "document",
            "doc": doc["_source"]
        }
