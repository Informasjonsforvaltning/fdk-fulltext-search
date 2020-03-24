import time

import pytest
from requests import post, get

from tests.contract.contract_utils import wait_for_es, populate, clean_es

service_url = "http://localhost:8080"


@pytest.fixture(scope="module")
def api():
    wait_for_es()
    populate()
    yield
    clean_es()


class TestSearchAll:
    @pytest.mark.contract
    def test_harvest_should_not_create_duplicates(self, api):
        harvest_response = post(service_url + "/harvest")
        if harvest_response.status_code != 200:
            raise Exception(
                'Test containers: received http status' + harvest_response.status_code + "when attempting to start harvest")
        amount_after_first_harvest = 130
        result = post(service_url + "/search")
        amount_after_second_harvest = result.json()["hits"]["total"]["value"]
        assert amount_after_second_harvest is amount_after_first_harvest

    @pytest.mark.contract
    def test_search_without_body_should_return_response_with_hits_aggregations_and_page(self, api):
        result = post(service_url + "/search").json()
        assert "hits" in result
        assert "aggregations" in result
        assert "page" in result

    @pytest.mark.contract
    def test_search_without_body_should_return_list_of_content_with_authority_boost(self, api):
        result = post(service_url + "/search").json()["hits"]
        previous_was_authority = True
        for hits in result:
            if "nationalComponent" in hits:
                if hits["nationalComponent"]:
                    assert previous_was_authority is True
                    previous_was_authority = True
                else:
                    previous_was_authority = False
            elif "provenance" in hits:
                if hits["provenance"]["code"] == "NASJONAL":
                    assert previous_was_authority is True
                    previous_was_authority = True
                else:
                    previous_was_authority = False
            else:
                previous_was_authority = False

