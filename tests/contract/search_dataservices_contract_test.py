import json
import time
from datetime import datetime
import pytest
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError
from jsonpath_ng import parse

from tests.contract.contract_utils import expected_page_keys
from tests.contract.search_all_contract_test import service_url

indices_name = "dataservices"
data_type = "dataservice"
data_services_url = service_url + f"/{indices_name}"
es_dataservice_url = "http://localhost:9200/dataservices"


@pytest.fixture(scope="function")
def wait_for_dataservice_ready():
    timeout = time.time() + 90
    try:
        while True:
            response = requests.get(es_dataservice_url + "/_count")
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


class TestDataServiceSearch:
    @pytest.mark.contract
    def test_response_should_have_correct_content(
        self, docker_service, api, wait_for_dataservice_ready
    ):
        result = requests.post(data_services_url)
        assert result.status_code == 200
        result_json = result.json()
        content_keys = result_json.keys()
        assert "hits" in content_keys
        result_data_types = [
            match.value for match in parse("hits[*].type").find(result_json["hits"])
        ]
        for dt in result_data_types:
            assert dt == data_type
        assert "page" in content_keys
        page_key_matches = list(
            set(result_json["page"].keys()) & set(expected_page_keys)
        )
        assert page_key_matches.__len__() == expected_page_keys.__len__()
        assert "aggregations" in content_keys
        aggregations = result_json["aggregations"]
        agg_keys = aggregations.keys()
        assert "orgPath" in agg_keys
        assert len(aggregations["orgPath"]["buckets"]) > 0
        assert "formats" in agg_keys
        assert len(aggregations["formats"]["buckets"]) > 0

    @pytest.mark.contract
    def test_should_have_correct_size_and_page(
        self, docker_service, api, wait_for_dataservice_ready
    ):
        result = requests.post(data_services_url)
        assert result.status_code == 200
        default_result_json = result.json()
        assert default_result_json["page"]["size"] == 10
        assert default_result_json["page"]["currentPage"] == 0
        page_request_body = {"page": 1}
        page_result = requests.post(url=data_services_url, json=page_request_body)
        assert page_result.status_code == 200
        page_result_json = page_result.json()

        assert page_result_json["page"]["size"] == 3
        assert page_result_json["page"]["currentPage"] == 1
        assert json.dumps(default_result_json["hits"][0]) != json.dumps(
            page_result_json["hits"][0]
        )

    @pytest.mark.contract
    def test_should_sort_on_date(self, docker_service, api, wait_for_dataservice_ready):
        body = {"sorting": {"field": "harvest.firstHarvested", "direction": "desc"}}
        result = requests.post(url=data_services_url, json=body)
        assert result.status_code == 200
        last_date = None
        for hit in result.json()["hits"]:
            date = hit["harvest"]["firstHarvested"].split("+")[0]
            if last_date:
                assert datetime.strptime(
                    date, "%Y-%m-%dT%H:%M:%SZ"
                ) <= datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%SZ")
            last_date = date

    @pytest.mark.contract
    def test_should_filter_on_orgPath(
        self, docker_service, api, wait_for_datasets_ready
    ):
        org_path = "PRIVAT/910244132"
        body = {"filters": [{"orgPath": org_path}]}
        result = requests.post(url=data_services_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json()["hits"]
        assert len(result_json_hits) == 5
        for hit in result_json_hits:
            assert org_path in hit["publisher"]["orgPath"]

    @pytest.mark.contract
    def test_get_single_data_service_with_id_search(
        self, docker_service, api, wait_for_datasets_ready
    ):
        body = {"filters": [{"_id": "d1d698ef-267a-3d57-949f-b2bc44657f3e"}]}
        result = requests.post(url=data_services_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json()["hits"]
        assert len(result_json_hits) == 1
        assert result_json_hits[0].get("id") == "d1d698ef-267a-3d57-949f-b2bc44657f3e"


def get_time(timestamp: str):
    return datetime.strptime(timestamp.split("T")[0], "%Y-%M-%d")
