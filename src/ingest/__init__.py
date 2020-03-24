# TODO : setup rabbit listeners; "update_es": [informationmodels,concepts,datasets,dataservices]
import requests
import os
from elasticsearch import Elasticsearch, helpers
from .utils import Indexes

ES_HOST = os.getenv('ELASTIC_HOST') or "localhost"
ES_PORT = os.getenv('ELASTIC_PORT') or "9200"
client = Elasticsearch([ES_HOST + ':' + ES_PORT])
API_URL = os.getenv('API_URL')


def fetch_information_models():
    print("fetching information models")
    info_url = API_URL + "informationmodels"
    r = requests.request(url=info_url, method="GET")
    documents = r.json()["_embedded"]["informationmodels"]
    elasticsearch_ingest(documents, Indexes.INFO_MODEL, Indexes.INFO_MODEL_ID_KEY)


def fetch_concepts():
    print("fetching concepts")
    concept_url = API_URL + "concepts"
    r = requests.request(url=concept_url, method="GET")
    documents = r.json()["_embedded"]["concepts"]
    elasticsearch_ingest(documents, Indexes.CONCEPTS, Indexes.CONCEPTS_ID_KEY)


def fetch_datasets():
    print("fetching datasets")
    dataset_url = API_URL + "datasets"
    r = requests.get(url=dataset_url, headers={"Accept": "application/json"})
    documents = r.json()["hits"]["hits"]
    elasticsearch_ingest_from_source(documents, Indexes.DATA_SETS, Indexes.DATA_SETS_ID_KEY)


def fetch_dataservices():
    print("fetching services")
    dataserve_url = API_URL + "apis"
    r = requests.get(url=dataserve_url, headers={"Accept": "application/json"})
    documents = r.json()["hits"]
    elasticsearch_ingest(documents, "dataservices", "id")



def elasticsearch_ingest(documents, index, id_key):
    result = helpers.bulk(client=client, actions=yield_documents(documents, index, id_key))


def elasticsearch_ingest_from_source(documents, index, id_key):
    result = helpers.bulk(client=client, actions=yield_documents_from_source(documents, index, id_key))


def yield_documents(documents, index, id_key):
    for doc in documents:
        print(doc)
        yield {
            "_index": index,
            "_type": "document",
            "_id": doc[id_key],
            "_source": doc
        }


def yield_documents_from_source(documents, index, id_key):
    for doc in documents:
        print(doc)
        yield {
            "_index": index,
            "_id": doc["_id"],
            "_type": "document",
            "_source": doc["_source"]
        }
