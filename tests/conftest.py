import os
import re
import time

import pytest
import requests
from requests import get
from urllib3.exceptions import MaxRetryError, NewConnectionError

from tests.contract.contract_utils import wait_for_es, populate

json_info_models = {"page": {"totalElements": 2},
                    "_embedded": {
                        "informationmodels": [
                            {
                                "id": 1234566
                            }
                        ]
                    }
                    }
json_concepts = {"page": {"totalElements": 2},
                 "_embedded": {
                     "concepts": [
                         {
                             "id": 1234566
                         }
                     ]
                 }
                 }
json_data_services = {
    "total": 2,
    "hits": [
        {
            "nationalComponent": "true",
            "isOpenAccess": "true",
            "isOpenLicense": "true",
            "isFree": "true",
            "statusCode": "EXPERIMENTAL",
            "id": "baaeeaf2-a2d0-44d0-a5a9-d040a66993e2",
            "title": "Sindres nasjonale opplæringskontorregister API",
            "publisher": {
                "id": "910244132",
                "name": "RAMSUND OG ROGNAN REVISJON",
                "orgPath": "/ANNET/910244132"
            }
        }
    ]
}


@pytest.fixture(scope="session")
def api():
    wait_for_es()
    populate()
    yield


@pytest.fixture(scope="function")
def wait_for_datasets_ready():
    timeout = time.time() + 90
    try:
        while True:
            response = get("http://localhost:8000/indices?name=datasets")
            if response.json()[0]['count'] >= 1252:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for fulltext-search, last response '
                    'was {0}'.format(response.json()["count"]))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test function setup: could not contact fdk-fulltext-search container')
    yield


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, text = None):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text

        def json(self):
            return self.json_data

        @staticmethod
        def raise_for_status():
            print("status check")

    response_json = {}
    response_text = ""
    if re.findall("informationmodels", kwargs['url']).__len__() > 0:
        response_json = json_info_models
    elif re.findall("concept", kwargs['url']).__len__() > 0:
        response_json = json_concepts
    elif re.findall("dataset", kwargs['url']).__len__() > 0:
        response_text = "@prefix dcat:  <http://www.w3.org/ns/dcat#> .\n\n<https://example.com/dataset/1234566>\n a dcat:Dataset ."
    elif re.findall("api", kwargs['url']).__len__() > 0:
        response_json = json_data_services
    return MockResponse(json_data=response_json,
                        status_code=200, text=response_text)


@pytest.fixture
def mock_ingest(mocker):
    return mocker.patch('src.ingest.elasticsearch_ingest')


@pytest.fixture
def mock_data_service_ingest(mocker):
    return mocker.patch('src.ingest.elasticsearch_ingest_data_service')


@pytest.fixture
def mock_ingest_from_source(mocker):
    return mocker.patch('src.ingest.elasticsearch_ingest_from_source')


@pytest.fixture
def mock_ingest_from_harvester(mocker):
    return mocker.patch('src.ingest.elasticsearch_ingest_from_harvester')


@pytest.fixture
def mock_get(mocker):
    return mocker.patch('src.ingest.requests.get', side_effect=mocked_requests_get)


@pytest.fixture
def mock_single_delete(mocker):
    return mocker.patch('src.ingest.es_client.indices.delete')


@pytest.fixture
def mock_single_create(mocker):
    return mocker.patch('src.ingest.es_client.indices.create')


@pytest.fixture
def mock_single_reindex(mocker):
    return mocker.patch('src.ingest.reindex_specific_index', return_value=None)


@pytest.fixture
def mock_dataset_parser(mocker):
    return mocker.patch('fdk_rdf_parser.parseDatasets', return_value={})


@pytest.fixture
def mock_env(monkeypatch):
    return monkeypatch.setattr(os, 'getcwd', mock_getcwd)


@pytest.fixture
def mock_count_elastic(mocker):
    return mocker.patch('elasticsearch.Elasticsearch.count',
                        return_value={
                            "count": 1090,
                            "_shards": {
                                "total": 1,
                                "successful": 1,
                                "skipped": 0,
                                "failed": 0
                            }
                        })


def mock_getcwd():
    pwd = os.getcwdb().decode("utf-8")
    return pwd.replace('/tests', '')


def empty_mock():
    return


@pytest.fixture(scope="function")
def wait_for_ready():
    timeout = time.time() + 90
    try:
        while True:
            response = get("http://localhost:8000/count")
            if response.json()['count'] >= 5569:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for poupulation of ElasticSearch, last response '
                    'was {0}'.format(response.json()["count"]))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test function setup: could not contact fdk-fulltext-search container')
    yield
