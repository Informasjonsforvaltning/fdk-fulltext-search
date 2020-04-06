import json
import re
from datetime import datetime

import pytest
from requests import post, get, put

from tests.contract.contract_utils import wait_for_es, populate

service_url = "http://localhost:8000"
data_types = ["dataservice", "dataset", "concept", "informationmodel"]


@pytest.fixture(scope="module")
def api():
    wait_for_es()
    populate()
    yield


class TestSearchAll:
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

    @pytest.mark.contract
    def test_hits_should_contain_search_string(self, api):
        body = {
            "q": "barnehage"
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            values = json.dumps(hit)
            prt1 = re.findall("barnehage", values)
            prt2 = re.findall("Barnehage", values)
            arr = prt1 + prt2
            assert (len(arr)) > 0

    @pytest.mark.contract
    def test_hits_should_be_filtered_on_orgPath(self, api):
        body = {
            "filters": [{"orgPath": "/PRIVAT"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert "PRIVAT" in hit["publisher"]["orgPath"]

    @pytest.mark.contract
    def test_hits_should_have_word_and_be_filtered_on_orgPath(self, api):
        body = {
            "q": "barnehage",
            "filters": [{"orgPath": "/KOMMUNE/840029212"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            values = json.dumps(hit)
            prt1 = re.findall("barnehage", values)
            prt2 = re.findall("Barnehage", values)
            arr = prt1 + prt2
            assert (len(arr)) > 0
            assert "/KOMMUNE/840029212" in hit["publisher"]["orgPath"]

    @pytest.mark.contract
    def test_hits_should_be_filtered_on_is_open_Access(self, api):
        body = {
            "filters": [{"isOpenAccess": "true"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["isOpenAccess"] is True

    @pytest.mark.contract
    def test_hits_should_have_word_and_be_filtered_on_is_not_open_Access(self, api):
        body = {
            "filters": [{"isOpenAccess": "false"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["isOpenAccess"] is False

    @pytest.mark.contract
    def test_hits_should_be_filtered_on_accessRights_PUBLIC(self, api):
        body = {
            "filters": [{"accessRights": "PUBLIC"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["accessRights"]["code"] == "PUBLIC"

    @pytest.mark.contract
    def test_hits_should_be_filtered_on_accessRights_NON_PUBLIC(self, api):
        body = {
            "filters": [{"accessRights": "NON_PUBLIC"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["accessRights"]["code"] == "NON_PUBLIC"

    @pytest.mark.contract
    def test_empty_request_after_request_with_q_should_return_default(self, api):
        body = {
            "q": "barn"
        }
        post(url=service_url + "/search", json=body)
        post(url=service_url + "/search", json=body)
        post(url=service_url + "/search", json=body)
        pre_request = post(url=service_url + "/search", json=body)
        result = post(url=service_url + "/search")
        assert json.dumps(pre_request.json()) != json.dumps(result.json())

    @pytest.mark.contract
    def test_sort_should_returns_the_most_recent_hits(self, api):
        body = {
            "sorting": {
                "field": "harvest.firstHarvested",
                "direction": "desc"
            }
        }
        result = post(url=service_url + "/search", json=body)
        last_date = None
        for hit in result.json()["hits"]:
            assert "harvest" in hit
            current_date = datetime.strptime(hit["harvest"]["firstHarvested"].split('T')[0], '%Y-%m-%d')
            if last_date is not None:
                assert current_date <= last_date
            last_date = current_date

    @pytest.mark.contract
    def test_sort_should_returns_the_most_recent_hits(self, api):
        body = {
            "sorting": {
                "field": "harvest.firstHarvested",
                "direction": "asc"
            }
        }
        result = post(url=service_url + "/search", json=body)
        last_date = None
        for hit in result.json()["hits"]:
            assert "harvest" in hit
            current_date = datetime.strptime(hit["harvest"]["firstHarvested"].split('T')[0], '%Y-%m-%d')
            if last_date is not None:
                assert current_date >= last_date
            last_date = current_date
