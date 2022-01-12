import os
import re
import time

from dotenv import load_dotenv
from flask import Flask
from flask.testing import FlaskClient
import pytest
import requests
from requests import get
from urllib3.exceptions import MaxRetryError, NewConnectionError

from fdk_fulltext_search import create_app
from tests.utils import populate, wait_for_es

turtle_concept = """@prefix dct:   <http://purl.org/dc/terms/> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix dcat:  <http://www.w3.org/ns/dcat#> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .

<http://testutgiver.no/begrep/111>
        a                             skos:Concept .

<https://testdirektoratet.no/concepts/321>
        a               dcat:CatalogRecord ;
        dct:identifier  "321" ;
        dct:issued      "2020-07-03T10:04:39.738Z"^^xsd:dateTime ;
        dct:modified    "2021-02-23T12:00:21.354Z"^^xsd:dateTime ;
        foaf:primaryTopic <http://testutgiver.no/begrep/111> .
"""

turtle_datasets = """
@prefix dct:   <http://purl.org/dc/terms/> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat:  <http://www.w3.org/ns/dcat#> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .

<https://testdirektoratet.no/datasets/123>
        a                  dcat:CatalogRecord ;
        dct:identifier     "123" ;
        dct:issued         "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        dct:modified       "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        foaf:primaryTopic  <https://testutgiver.no/datasets/987654321> .

<https://testutgiver.no/datasets/987654321>
        a                  dcat:Dataset ."""

turtle_dataservices = """
@prefix dct:   <http://purl.org/dc/terms/> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat:  <http://www.w3.org/ns/dcat#> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .

<https://testdirektoratet.no/dataservices/321>
        a                  dcat:CatalogRecord ;
        dct:identifier     "321" ;
        dct:issued         "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        dct:modified       "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        foaf:primaryTopic  <https://testutgiver.no/dataservices/987654321> .

<https://testutgiver.no/dataservices/987654321>
        a                  dcat:DataService ."""

turtle_models = """
@prefix dct:   <http://purl.org/dc/terms/> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat:  <http://www.w3.org/ns/dcat#> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .
@prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

<https://testdirektoratet.no/models/321>
        a                  dcat:CatalogRecord ;
        dct:identifier     "321" ;
        dct:issued         "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        dct:modified       "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        foaf:primaryTopic  <https://testutgiver.no/models/987654321> .

<https://testutgiver.no/models/987654321>
        a                  modelldcatno:InformationModel ."""

turtle_public_services = """
@prefix dct:   <http://purl.org/dc/terms/> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat:  <http://www.w3.org/ns/dcat#> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .
@prefix cpsv: <http://purl.org/vocab/cpsv#> .

<https://testdirektoratet.no/services/321>
        a                  dcat:CatalogRecord ;
        dct:identifier     "321" ;
        dct:issued         "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        dct:modified       "2020-06-22T13:39:27.334Z"^^xsd:dateTime ;
        foaf:primaryTopic  <https://testutgiver.no/services/987654321> .

<https://testutgiver.no/services/987654321>
        a                  cpsv:PublicService ."""


load_dotenv()
HOST_PORT = int(os.environ.get("HOST_PORT", "8000"))


def is_responsive(url):
    """Return true if response from service is 200."""
    url = f"{url}/ready"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            time.sleep(2)  # sleep extra 2 sec
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def docker_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("fdk-fulltext-search", HOST_PORT)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=120.0, pause=0.5, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Override default location of docker-compose.yml file."""
    return os.path.join(str(pytestconfig.rootdir), "./", "docker-compose.yml")


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
            if response.json()[0]["count"] >= 1252:
                break
            if time.time() > timeout:
                pytest.fail(
                    "Test function setup: timed out while waiting for fulltext-search, last response "
                    "was {0}".format(response.json()["count"])
                )
            time.sleep(1)
    except (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        MaxRetryError,
        NewConnectionError,
    ):
        pytest.fail(
            "Test function setup: could not contact fdk-fulltext-search container"
        )
    yield


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, text=None):
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

    req_url = kwargs.get("url")
    req_url = req_url if req_url else ""

    if re.findall("information-models", req_url).__len__() > 0:
        response_text = turtle_models
    elif re.findall("concepts", req_url).__len__() > 0:
        response_text = turtle_concept
    elif re.findall("datasets", req_url).__len__() > 0:
        response_text = turtle_datasets
    elif re.findall("data-services", req_url).__len__() > 0:
        response_text = turtle_dataservices
    elif re.findall("public-services", req_url).__len__() > 0:
        response_text = turtle_public_services
    return MockResponse(json_data=response_json, status_code=200, text=response_text)


@pytest.fixture
def mock_ingest(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.elasticsearch_ingest")


@pytest.fixture
def mock_ingest_from_source(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.elasticsearch_ingest_from_source")


@pytest.fixture
def mock_ingest_from_harvester(mocker):
    return mocker.patch(
        "fdk_fulltext_search.ingest.elasticsearch_ingest_from_harvester"
    )


@pytest.fixture
def mock_create_or_update_dataset_pipeline(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.create_or_update_dataset_pipeline")


@pytest.fixture
def mock_create_or_update_dataservice_pipeline(mocker):
    return mocker.patch(
        "fdk_fulltext_search.ingest.create_or_update_dataservice_pipeline"
    )


@pytest.fixture
def mock_get(mocker):
    return mocker.patch(
        "fdk_fulltext_search.ingest.requests.get", side_effect=mocked_requests_get
    )


@pytest.fixture
def mock_single_delete(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.es_client.indices.delete")


@pytest.fixture
def mock_single_create(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.es_client.indices.create")


@pytest.fixture
def mock_single_reindex(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.create_index", return_value=None)


@pytest.fixture
def mock_set_alias(mocker):
    return mocker.patch(
        "fdk_fulltext_search.ingest.set_alias_for_new_index", return_value=None
    )


@pytest.fixture
def mock_dataset_parser(mocker):
    return mocker.patch("fdk_rdf_parser.parse_datasets", return_value={})


@pytest.fixture
def mock_data_service_parser(mocker):
    return mocker.patch("fdk_rdf_parser.parse_data_services", return_value={})


@pytest.fixture
def mock_model_parser(mocker):
    return mocker.patch("fdk_rdf_parser.parse_information_models", return_value={})


@pytest.fixture
def mock_env(monkeypatch):
    return monkeypatch.setattr(os, "getcwd", mock_getcwd)


@pytest.fixture
def mock_count_elastic(mocker):
    return mocker.patch(
        "elasticsearch.Elasticsearch.count",
        return_value={
            "count": 1090,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
        },
    )


def mock_getcwd():
    pwd = os.getcwdb().decode("utf-8")
    return pwd.replace("/tests", "")


def empty_mock():
    return


@pytest.fixture(scope="function")
def wait_for_ready():
    timeout = time.time() + 90
    try:
        while True:
            response = get("http://localhost:8000/count")
            if response.json()["count"] >= 5537:
                break
            if time.time() > timeout:
                pytest.fail(
                    "Test function setup: timed out while waiting for poupulation of ElasticSearch, last response "
                    "was {0}".format(response.json()["count"])
                )
            time.sleep(5)
    except (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        MaxRetryError,
        NewConnectionError,
    ):
        pytest.fail(
            "Test function setup: could not contact fdk-fulltext-search container"
        )
    yield


@pytest.mark.integration
@pytest.fixture
def app():
    """Returns a Flask app for integration testing."""
    app = create_app({"TESTING": True})

    yield app


@pytest.mark.integration
@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Returns a client for integration testing."""
    return app.test_client()


@pytest.fixture(scope="function")
def wait_for_concepts():
    timeout = time.time() + 90
    try:
        while True:
            response = get("http://localhost:8000/indices?name=concepts")
            if response.json()[0]["count"] >= 530:
                break
            if time.time() > timeout:
                pytest.fail(
                    "Test function setup: timed out while waiting for fulltext-search, last response "
                    "was {0}".format(response.json()["count"])
                )
            time.sleep(1)
    except (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        MaxRetryError,
        NewConnectionError,
    ):
        pytest.fail(
            "Test function setup: could not contact fdk-fulltext-search container"
        )
    yield


@pytest.fixture(scope="function")
def wait_for_dataservice_ready():
    timeout = time.time() + 90
    try:
        while True:
            response = requests.get("http://localhost:9200/dataservices/_count")
            if response.json()["count"] >= 13:
                break
            if time.time() > timeout:
                pytest.fail(
                    "Test function setup: timed out while waiting for poupulation of ElasticSearch, last response "
                    "was {0}".format(response.json()["count"])
                )
            time.sleep(1)
    except (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        MaxRetryError,
        NewConnectionError,
    ):
        pytest.fail("Test function setup: could not contact elasticsearch container")
    yield


@pytest.fixture(scope="function")
def wait_for_information_models():
    timeout = time.time() + 90
    try:
        while True:
            response = get("http://localhost:8000/indices?name=informationmodels")
            if response.json()[0]["count"] >= 4:
                break
            if time.time() > timeout:
                pytest.fail(
                    "Test function setup: timed out while waiting for fulltext-search, last response "
                    "was {0}".format(response.json()["count"])
                )
            time.sleep(1)
    except (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        MaxRetryError,
        NewConnectionError,
    ):
        pytest.fail(
            "Test function setup: could not contact fdk-fulltext-search container"
        )
    yield
