import time

import pytest
import requests
from jsonpath_ng import parse
from requests import get
from urllib3.exceptions import MaxRetryError, NewConnectionError

from tests.contract.contract_utils import expected_page_keys
from tests.contract.search_contract_test import service_url


@pytest.fixture(scope="function")
def wait_for_information_models():
    timeout = time.time() + 90
    try:
        while True:
            response = get("http://localhost:8000/indices?name=informationmodels")
            if response.json()[0]['count'] >= 530:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for fulltext-search, last response '
                    'was {0}'.format(response.json()["count"]))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test function setup: could not contact fdk-fulltext-search container')
    yield


indices_name = "informationmodels"
data_type = "informationmodel"
informationmodel_url = service_url + indices_name


class TestInformationModelSearch:

    @pytest.mark.contract
    def test_response_should_have_correct_content(self, api, wait_for_information_models):
        result = requests.post(informationmodel_url)
        result_json = result.json()
        content_keys = result_json.keys()
        assert result_json.status_code == 200
        assert "hits" in content_keys
        result_data_types = [match.value for match in parse("type").find(result_json["hits"])]
        for dt in result_data_types:
            assert dt == data_type
        assert "page" in content_keys
        page_key_matches = list(set(result_json["page"].keys()) & set(expected_page_keys))
        assert page_key_matches.__len__() == expected_page_keys.__len__()
        assert "aggregations" in content_keys
        agg_keys = result_json["aggregations"].keys()
        assert "los" in agg_keys
        assert "orPath" in agg_keys

    @pytest.mark.contract
    def test_hits_should_be_correctly_sorted_on_title(self):
        """
            1. exact match
            2. word in title
        """
        search_str = "RA-0554 Pris på juridisk tjenesteyting"
        body = {
            "q": search_str,
            "size": 300
        }
        result = requests.post(url=informationmodel_url, body=body)
        assert result.status_code == 200
        result_json = result.json()
        last_was_exact_match = True
        last_was_partial_match_in_title = False
        for hit in result_json["hits"]:
            if is_exact_match_in_title(hit, search_str):
                assert last_was_exact_match
                last_was_exact_match = True
            elif is_partial_match_in_title(hit, search_str):
                assert last_was_exact_match or last_was_partial_match_in_title
                last_was_exact_match = False
                last_was_partial_match_in_title = True
            else:
                last_was_exact_match = False
                last_was_partial_match_in_title = False


def is_exact_match_in_title(hit, search_str):
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


def is_partial_match_in_title(hit, search_str):
    title = hit["title"]
    keys = title.keys()
    has_exact_match = False
    if "nb" in keys:
        for word in title["nb"].split():
            if word in search_str:
                has_exact_match = True
    if "nn" in keys:
        for word in title["nn"].split():
            if word in search_str:
                has_exact_match = True
    if "no" in keys:
        for word in title["no"].split():
            if word in search_str:
                has_exact_match = True
    if "en" in keys:
        for word in title["en"].split():
            if word in search_str:
                has_exact_match = True
    return has_exact_match
