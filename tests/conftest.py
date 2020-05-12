import os
import re

import pytest

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
json_data_sets = {
    "hits": {
        "total": 2,
        "hits": [
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


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            print("status check")

    response_json = {}
    if re.findall("informationmodels", kwargs['url']).__len__() > 0:
        response_json = json_info_models
    elif re.findall("concept", kwargs['url']).__len__() > 0:
        response_json = json_concepts
    elif re.findall("dataset", kwargs['url']).__len__() > 0:
        response_json = json_data_sets
    elif re.findall("api", kwargs['url']).__len__() > 0:
        response_json = json_data_services
    return MockResponse(json_data=response_json,
                        status_code=200)


@pytest.fixture
def mock_ingest(mocker):
    return mocker.patch('src.ingest.elasticsearch_ingest')


@pytest.fixture
def mock_ingest_from_source(mocker):
    return mocker.patch('src.ingest.elasticsearch_ingest_from_source')


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
