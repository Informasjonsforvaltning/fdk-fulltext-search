from datetime import datetime
import json
import re
import time

from jsonpath_ng import parse
import pytest
import requests
from requests import get
from urllib3.exceptions import MaxRetryError, NewConnectionError

from tests.contract.contract_utils import expected_page_keys
from tests.contract.search_all_contract_test import service_url


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


indices_name = "informationmodels"
data_type = "informationmodel"
informationmodel_url = service_url + f"/{indices_name}"


class TestInformationModelSearch:
    @pytest.mark.contract
    def test_response_should_have_correct_content(
        self, docker_service, api, wait_for_information_models
    ):
        result = requests.post(informationmodel_url)
        result_json = result.json()
        content_keys = result_json.keys()
        assert result.status_code == 200
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
        agg_keys = result_json["aggregations"].keys()
        assert "los" in agg_keys
        assert "orgPath" in agg_keys

    @pytest.mark.contract
    def test_hits_should_be_correctly_sorted_on_title(
        self, docker_service, api, wait_for_information_models
    ):
        """
        1. exact match
        2. word in title
        """
        search_str = "di"
        body = {"q": search_str, "size": 300}
        result = requests.post(url=informationmodel_url, json=body)
        assert result.status_code == 200
        result_json = result.json()
        last_was_exact_match = True
        last_was_partial_match_in_title = False
        for hit in result_json["hits"]:
            if has_exact_match_in_title(hit, search_str):
                assert last_was_exact_match
                last_was_exact_match = True
            elif has_partial_match_in_title(hit, search_str):
                assert last_was_exact_match or last_was_partial_match_in_title
                last_was_exact_match = False
                last_was_partial_match_in_title = True
            else:
                last_was_exact_match = False
                last_was_partial_match_in_title = False

    @pytest.mark.contract
    def test_should_filter_on_org_path(
        self, docker_service, api, wait_for_information_models
    ):
        org_path = "STAT/972417858/991825827"
        body = {"filters": [{"orgPath": org_path}]}
        result = requests.post(url=informationmodel_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json()["hits"]
        assert len(result_json_hits) > 0
        for hit in result_json_hits:
            assert org_path in hit["publisher"]["orgPath"]

    @pytest.mark.contract
    def test_should_filter_on_los(
        self, docker_service, api, wait_for_information_models
    ):
        los_path = "bygg-og-eiendom"
        body = {"filters": [{"los": los_path}]}
        result = requests.post(url=informationmodel_url, json=body)
        assert result.status_code == 200
        result_hits = result.json()["hits"]
        assert len(result_hits) == 2
        for hit in result_hits:
            los_paths = ",".join(
                [",".join(los_theme["losPaths"]) for los_theme in hit["losTheme"]]
            )
            assert los_path in los_paths

    @pytest.mark.contract
    def test_should_filter_on_several_los_themes(
        self, docker_service, api, wait_for_information_models
    ):
        los_path_1 = "helse-og-omsorg"
        los_path_2 = "bygg-og-eiendom"
        body = {"filters": [{"los": f"{los_path_1},{los_path_2}"}]}

        result = requests.post(url=informationmodel_url, json=body)
        result_json = result.json()
        assert result.status_code == 200
        assert len(result_json["hits"]) == 1
        for hit in result_json["hits"]:
            los_paths = ",".join(
                [",".join(los_theme["losPaths"]) for los_theme in hit["losTheme"]]
            )
            assert los_path_1 in los_paths
            assert los_path_2 in los_paths

    @pytest.mark.contract
    def test_should_filter_on_los_and_org_path(
        self, docker_service, api, wait_for_information_models
    ):
        org_path = "STAT"
        los_path = "bygg-og-eiendom"
        body = {"filters": [{"orgPath": org_path}, {"los": los_path}]}
        result = requests.post(url=informationmodel_url, json=body)
        result_json = result.json()
        assert result.status_code == 200
        assert len(result_json["hits"]) > 0
        for hit in result_json["hits"]:
            assert org_path in hit["publisher"]["orgPath"]

    @pytest.mark.contract
    def test_should_have_correct_size_and_page(
        self, docker_service, api, wait_for_information_models
    ):
        default_result = requests.post(informationmodel_url).json()
        assert default_result["page"]["size"] == 4
        assert default_result["page"]["currentPage"] == 0

        page_request_body = {"page": 1, "size": 2}
        page_result = requests.post(
            url=informationmodel_url, json=page_request_body
        ).json()
        assert page_result["page"]["size"] == 2
        assert page_result["page"]["currentPage"] == 1

        assert json.dumps(default_result["hits"][0]) != json.dumps(
            page_result["hits"][0]
        )

    @pytest.mark.contract
    def test_should_sort_on_date(
        self, docker_service, api, wait_for_information_models
    ):
        body = {"sorting": {"field": "harvest.firstHarvested", "direction": "desc"}}
        result = requests.post(url=informationmodel_url, json=body)
        assert result.status_code == 200
        last_date = None
        for hit in result.json()["hits"]:
            date = hit["harvest"]["firstHarvested"]
            if last_date:
                assert datetime.strptime(
                    date, "%Y-%m-%dT%H:%M:%SZ"
                ) <= datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%SZ")
            last_date = date


def has_exact_match_in_title(hit, search_str):
    title = hit["title"]
    keys = title.keys()
    has_exact_match = False
    if "nb" in keys and title["nb"] == search_str:
        has_exact_match = True
    if "nn" in keys and title["nb"] == search_str:
        has_exact_match = True
    if "no" in keys and title["nb"] == search_str:
        has_exact_match = True
    if "en" in keys and title["nb"] == search_str:
        has_exact_match = True
    return has_exact_match


def has_partial_match_in_title(hit, search_str):
    title = hit["title"]
    prt1 = re.findall(search_str.lower(), json.dumps(title).lower())
    if len(prt1) > 0:
        return True
    else:
        return False
