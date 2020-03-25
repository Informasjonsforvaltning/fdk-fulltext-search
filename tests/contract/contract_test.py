import pytest
from requests import post, get

from tests.contract.contract_utils import wait_for_es, populate, clean_es

service_url = "http://localhost:8080"
data_types = ["dataservice", "dataset", "concept", "informationmodel"]

@pytest.fixture(scope="module")
def api():
    wait_for_es()
    populate()
    yield
    clean_es()


class TestSearchAll:
    @pytest.mark.contract
    def test_harvest_should_not_create_duplicates(self, api):
        amount_after_first_harvest = get(service_url + "/count").json()["count"]

        update_response = post(service_url + "/update")
        if update_response.status_code != 200:
            raise Exception(
                'Test containers: received http status' + update_response.status_code + "when attempting to start second"
                                                                                        "update")
        result = get(service_url + "/count").json()["count"]
        assert result is amount_after_first_harvest

    @pytest.mark.contract
    def test_search_without_body_should_return_response_with_hits_aggregations_and_page(self, api):
        result = post(service_url + "/search").json()
        hasHits = False
        hasAggregation = False
        hasPage = False
        unknownItems = []
        for k, v in result.items():
            if k == "hits":
                hasHits = True
            elif k == "aggregations":
                hasAggregation = True
            elif k == "page":
                hasPage = True
            else:
                unknownItems.append(k)
        assert hasHits is True
        assert hasAggregation is True
        assert hasPage is True
        assert len(unknownItems) is 0

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

    @pytest.mark.contract
    def test_search_without_body_should_contain_default_aggs(self, api):
        result = post(service_url + "/search").json()["aggregations"]
        keys = result.keys()
        assert "los" in keys
        assert "orgPath" in keys
        assert "isOpenAccess" in keys
        assert "accessRights" in keys
        assert len(result["los"]["buckets"]) > 0
        assert len(result["orgPath"]["buckets"]) > 0
        assert len(result["isOpenAccess"]["buckets"]) > 0
        assert len(result["accessRights"]["buckets"]) > 0

    @pytest.mark.contract
    def test_all_hits_should_have_type(self, api):
        result = post(service_url + "/search").json()["hits"]
        for hit in result:
            assert "type" in hit.keys()
            assert hit["type"] in data_types

    @pytest.mark.contract
    def test_hits_should_have_object_without_es_data(self, api):
        result = post(service_url + "/search").json()["hits"]
        for hit in result:
            assert "_type" not in hit.keys()
            assert "_source" not in hit.keys()

