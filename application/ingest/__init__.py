# TODO : setup rabitt listeners; "new_harvest": [informationmodels,concepts,datasets,dataservices]
import requests
import os
from elasticsearch import Elasticsearch, helpers

client = Elasticsearch()


def fetch_information_models():
    print("fetching information models")
    info_url = "https://www.staging.fellesdatakatalog.digdir.no/api/informationmodels?size=569"
    r = requests.request(url=info_url, method="GET")
    documents = r.json()["_embedded"]["informationmodels"]
    elasticsearch_ingest(documents, "informationmodels")


def fetch_concepts():
    print("fetching concepts")
    concept_url = "https://www.staging.fellesdatakatalog.digdir.no/api/concepts?size=3608"
    r = requests.request(url=concept_url, method="GET")
    documents = r.json()["_embedded"]["concepts"]
    elasticsearch_ingest(documents, "concepts")


def fetch_datasets():
    print("fetching datasets")
    dataset_url = "https://www.staging.fellesdatakatalog.digdir.no/api/datasets"
    r = requests.get(url=dataset_url, headers={"Accept":"application/json"})
    documents = r.json()["hits"]
    elasticsearch_ingest(documents, "datasets")


def fetch_dataservices():
    print("fetching services")
    dataserve_url = "https://www.staging.fellesdatakatalog.digdir.no/api/apis?size=3608"
    r = requests.get(url=dataserve_url, headers={"Accept":"application/json"})
    documents = r.json()["hits"]
    elasticsearch_ingest(documents, "dataservices")


def elasticsearch_ingest(documents, index):
    result = helpers.bulk(client=client, actions=yield_documents(documents, index))


def yield_documents(documents, index):
    for doc in documents:
        yield {
            "_index": index,
            "_type": "document",
            "doc": doc
        }
