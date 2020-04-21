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
        assert len(hits) > 0

    @pytest.mark.contract
    def test_search_without_body_should_contain_default_aggs(self, api):
        result = post(service_url + "/search").json()["aggregations"]
        keys = result.keys()
        assert "los" in keys
        assert "orgPath" in keys
        assert "availability" in keys
        assert "accessRights" in keys
        assert "opendata" in keys
        assert len(result["los"]["buckets"]) > 0
        assert len(result["orgPath"]["buckets"]) > 0
        assert len(result["availability"]["buckets"]) == 3
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
    def test_hits_should_start_with_exact_matches_in_title(self, api):
        srch_string = "enhetsregisteret"
        body = {
            "q": "enhetsregisteret",
            "size": 1000
        }
        last_was_exact = True
        exact_matches = 0
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            if "prefLabel" in hit:
                prefLabels = hit["prefLabel"]
                if is_exact_match(prefLabels.keys(), prefLabels, srch_string):
                    assert last_was_exact
                    exact_matches += 1
                else:
                    last_was_exact = False
            elif "title" in hit:
                title = hit["title"]
                if isinstance(title, dict):
                    if is_exact_match(title.keys(), title, srch_string):
                        assert last_was_exact
                        exact_matches += 1
                    else:
                        last_was_exact = False
                else:
                    if title.lower() == srch_string:
                        assert last_was_exact
                        exact_matches += 1
                    else:
                        last_was_exact = False
        assert exact_matches > 0

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

    @pytest.mark.contract
    def test_trailing_white_space_should_not_affect_result(self):
        body_no_white_space = {
            "q": "landbruk"
        }
        body_white_space = {
            "q": "landbruk  "
        }

        no_white_space_result = post(url=service_url + "/search", json=body_no_white_space).json()
        white_space_result = post(url=service_url + "/search", json=body_white_space).json()
        assert json.dumps(no_white_space_result["page"]) == json.dumps(no_white_space_result["page"])
        assert json.dumps(no_white_space_result["aggregations"]) == json.dumps(white_space_result["aggregations"])
        assert json.dumps(no_white_space_result["hits"][0]) == json.dumps(white_space_result["hits"][0])

    @pytest.mark.contract
    def test_words_in_title_after_exact_match(self, api):
        body = {
            "q": "barnehage",
            "size": 300
        }
        result = post(url=service_url + "/search", json=body)
        last_was_in_title = False
        last_not_in_title = False
        for hit in result.json()["hits"]:
            is_exact = is_exact_match_in_title(hit, "barnehage")
            if is_exact:
                assert last_was_in_title is False
                assert last_not_in_title is False
            elif is_word_title(hit, "barnehage"):
                assert last_not_in_title is False
                last_was_in_title = True
            else:
                last_not_in_title = True
                last_was_in_title = False

    @pytest.mark.contract
    def test_filter_on_los_should_have_informationmodels_and_datasets(self, api):
        body = {
            "filters": [
                {"los": "helse-og-omsorg"}
            ],
            "size": 100
        }
        result = post(url=service_url + "/search", json=body)
        has_info_models = False
        has_datasets = False
        for hit in result.json()["hits"]:
            if hit["type"] == "informationmodel":
                has_info_models = True
            elif hit["type"] == "dataset":
                has_datasets = True
            if has_info_models and has_datasets:
                break

        assert has_datasets is True
        assert has_info_models is True


def is_exact_match(keys, hit, search):
    for key in keys:
        if hit[key].lower() == search:
            return True
    return False


def is_exact_match_in_title(hit, srch_string):
    if "prefLabel" in hit:
        prefLabels = hit["prefLabel"]
        if is_exact_match(prefLabels.keys(), prefLabels, srch_string):
            return True
    elif "title" in hit:
        title = hit["title"]
        if isinstance(title, dict):
            if is_exact_match(title.keys(), title, srch_string):
                return True
        else:
            if title.lower() == srch_string:
                return True
    return False


def is_word_title(hit, srch_string):
    if "prefLabel" in hit:
        prefLabels = hit["prefLabel"]
        prt1 = re.findall(srch_string.lower(), json.dumps(prefLabels).lower())
        if len(prt1) > 0:
            return True
    elif "title" in hit:
        title = hit["title"]
        prt1 = re.findall(srch_string.lower(), json.dumps(title).lower())
        if len(prt1) > 0:
            return True
    return False
