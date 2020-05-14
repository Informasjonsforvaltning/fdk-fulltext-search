import json
import re
from datetime import datetime

import pytest
from jsonpath_ng import parse
from requests import post

service_url = "http://localhost:8000"
data_types = ["dataservice", "dataset", "concept", "informationmodel"]


class TestSearchAll:

    @pytest.mark.contract
    def test_search_without_body_should_return_response_with_hits_aggregations_and_page(self, api, wait_for_ready):
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
    def test_search_without_query_should_have_correct_sorting(self, api, wait_for_ready):
        """ 
            1. open authoritative datasets
            2. authoritative datasets
            3. authoritative dataservices
        """
        opts = {
            "size": 200
        }
        result = post(url=service_url + "/search", json=opts).json()["hits"]

        assert len(result) > 0
        debug_values = {
            "authority": [],
            "previous_dataset": [],
            "datatype": []
        }
        previous_was_dataset = True
        previous_was_open_data = True
        previous_was_authority = True
        for hits in result:
            if "nationalComponent" in hits:
                if hits["nationalComponent"]:
                    assert previous_was_authority is True, "nationalCompoent dataservice encountered after " \
                                                           "non-authoritative hit {0}".format(json.dumps(debug_values))
                    previous_was_authority = True
                else:
                    previous_was_authority = False
            elif "provenance" in hits:
                if hits["provenance"]["code"] == "NASJONAL":
                    assert previous_was_dataset is True, "dataset with NASJONAL provenance encountered after other " \
                                                         "data types {0}".format(json.dumps(debug_values))
                    assert previous_was_authority is True, "dataset with NASJONAL provenance encountered after " \
                                                           "non-authoritative hit {0}".format(json.dumps(debug_values))
                    if hits["accessRights"]["code"] == "PUBLIC":
                        openLicence = [match.value for match in parse("distribution[*].openLicense").find(hits)]
                        if True in openLicence:
                            assert previous_was_open_data, "open dataset encountered after non-open dataset dataset"
                            previous_was_open_data = True
                        else:
                            previous_was_open_data = False
                    previous_was_authority = True
                else:
                    previous_was_authority = False
            else:
                previous_was_authority = False
            previous_was_dataset = hits['type'] == 'dataset'
            debug_values["authority"].append(previous_was_authority)
            debug_values["previous_dataset"].append(previous_was_dataset)
            debug_values["datatype"].append(hits['type'])

    @pytest.mark.contract
    def test_search_without_body_should_contain_default_aggs(self, api, wait_for_ready):
        result = post(service_url + "/search").json()["aggregations"]
        keys = result.keys()
        assert "los" in keys
        assert "orgPath" in keys
        assert "availability" in keys
        assert "accessRights" in keys
        assert "opendata" in keys
        assert "theme" in keys
        assert len(result["los"]["buckets"]) > 0
        assert len(result["orgPath"]["buckets"]) > 0
        assert len(result["availability"]["buckets"]) == 3
        assert len(result["accessRights"]["buckets"]) > 0
        assert len(result["theme"]["buckets"]) > 0

    @pytest.mark.contract
    def test_all_hits_should_have_type(self, api, wait_for_ready):
        result = post(service_url + "/search").json()["hits"]
        for hit in result:
            assert "type" in hit.keys()
            assert hit["type"] in data_types

    @pytest.mark.contract
    def test_hits_should_have_object_without_es_data(self, api, wait_for_ready):
        result = post(service_url + "/search").json()["hits"]
        for hit in result:
            assert "_type" not in hit.keys()
            assert "_source" not in hit.keys()

    @pytest.mark.contract
    def test_hits_should_start_with_exact_matches_in_title(self, api, wait_for_ready):
        srch_string = "dokument"
        body = {
            "q": "dokument",
            "size": 1000
        }
        last_was_exact = True
        exact_matches = 0
        position = 0
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            if "prefLabel" in hit:
                prefLabels = hit["prefLabel"]
                if is_exact_match(prefLabels.keys(), prefLabels, srch_string):
                    assert last_was_exact, "exact match found at position {0}".format(position)
                    exact_matches += 1
                else:
                    last_was_exact = False
            elif "title" in hit:
                title = hit["title"]
                if isinstance(title, dict):
                    if is_exact_match(title.keys(), title, srch_string):
                        assert last_was_exact, "exact match found at position {0}".format(position)
                        exact_matches += 1
                    else:
                        last_was_exact = False
                else:
                    if title.lower() == srch_string:
                        assert last_was_exact, "exact match found at position {0}".format(position)
                        exact_matches += 1
                    else:
                        last_was_exact = False
            position += 1
        assert exact_matches > 0

    @pytest.mark.contract
    def test_hits_should_contain_search_string(self, api, wait_for_ready):
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
    def test_search_on_several_words_should_include_partial_matches_in_title(self, api, wait_for_ready):
        search_str = "Test for los"
        body = {
            "q": search_str,
            "size": "100"
        }
        result = post(url=service_url + "/search", json=body).json()
        assert result['page']['totalElements'] > 1
        data_type_count = {
            "dataservice": 0,
            "dataset": 0,
            "informationmodel": 0,
            "concept": 0
        }
        match_type_count = {
            "complete": 0,
            "one_word": 0,
            "two_words": 0
        }

        for hit in result["hits"]:
            data_type = hit["type"]
            data_type_count[data_type] += 1
            words_in_title = re.findall(r'\w+', get_title_values(hit).lower())
            matches = list(set(words_in_title) & set(search_str.lower().split())).__len__()
            if matches == 3:
                match_type_count["complete"] += 1
            elif matches == 2:
                match_type_count["two_words"] += 1
            elif matches == 1:
                match_type_count["one_word"] += 1

        assert match_type_count["one_word"] > 0, "No one word matches for {0}".format(search_str)
        assert match_type_count["two_words"] > 0, "No two word matches for {0}".format(search_str)

    @pytest.mark.contract
    def test_hits_should_be_filtered_on_orgPath(self, api, wait_for_ready):
        body = {
            "filters": [{"orgPath": "/PRIVAT"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert "PRIVAT" in hit["publisher"]["orgPath"]

    @pytest.mark.contract
    def test_hits_should_have_word_and_be_filtered_on_orgPath(self, api, wait_for_ready):
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
    def test_hits_should_be_filtered_on_is_open_Access(self, api, wait_for_ready):
        body = {
            "filters": [{"isOpenAccess": "true"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["isOpenAccess"] is True

    @pytest.mark.contract
    def test_hits_should_have_word_and_be_filtered_on_is_not_open_Access(self, api, wait_for_ready):
        body = {
            "filters": [{"isOpenAccess": "false"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["isOpenAccess"] is False

    @pytest.mark.contract
    def test_hits_should_be_filtered_on_accessRights_PUBLIC(self, api, wait_for_ready):
        body = {
            "filters": [{"accessRights": "PUBLIC"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["accessRights"]["code"] == "PUBLIC"

    @pytest.mark.contract
    def test_hits_should_be_filtered_on_accessRights_NON_PUBLIC(self, api, wait_for_ready):
        body = {
            "filters": [{"accessRights": "NON_PUBLIC"}]
        }
        result = post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["accessRights"]["code"] == "NON_PUBLIC"

    @pytest.mark.contract
    def test_empty_request_after_request_with_q_should_return_default(self, api, wait_for_ready):
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
    def test_sort_should_returns_the_most_recent_hits(self, api, wait_for_ready):
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
    def test_sort_should_returns_the_most_recent_hits(self, api, wait_for_ready):
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
    def test_trailing_white_space_should_not_affect_result(self, api, wait_for_ready):
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
    def test_words_in_title_after_exact_match(self, api, wait_for_ready):
        body = {
            "q": "barnehage",
            "size": 300
        }
        result = post(url=service_url + "/search", json=body)
        last_was_word_in_title = False
        last_was_not_word_in_title = False
        last_title = {}
        for hit in result.json()["hits"]:
            is_exact = is_exact_match_in_title(hit, "barnehage")
            if is_exact:
                assert last_was_word_in_title is False, "{0}: word in title encountered before exact " \
                                                        "matches in title".format(get_title_values(hit))
                assert last_was_not_word_in_title is False, "{0}: word not in title encountered before exact " \
                                                            "matches in title".format(get_title_values(hit))
            elif has_word_in_title(hit, "barnehage", ["barne", "hage"]):
                assert last_was_not_word_in_title is False, "{0}: word not in title encountered before word in title." \
                                                            "Last title was: {1}".format(get_title_values(hit),
                                                                                         last_title)
                last_was_word_in_title = True
            else:
                last_was_not_word_in_title = True
                last_was_word_in_title = False
            last_title = get_title_values(hit)

    @pytest.mark.contract
    def test_filter_on_los_should_have_informationmodels_and_datasets(self, api, wait_for_ready):
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

    @pytest.mark.contract
    def test_filter_on_los_should_handle_filters_on_different_themes(self, api, wait_for_ready):
        body = {
            "filters": [
                {"los": "helse-og-omsorg,naring"},
            ],
        }
        result = post(service_url + "/search", json=body)
        assert len(result.json()["hits"]) > 0

    @pytest.mark.contract
    def test_filter_on_los_should_handle_filters_om_sub_themes(self, api, wait_for_ready):
        body = {
            "filters": [
                {"los": "helse-og-omsorg,helse-og-omsorg/svangerskap"},
            ],
        }
        result = post(service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0

    @pytest.mark.contract
    def test_filter_on_los_themes_should_not_change_subtheme_content(self, api, wait_for_ready):
        empty_search = post(service_url + "/search").json()
        expected_themes = []
        for path in empty_search["aggregations"]["los"]["buckets"]:
            if len(re.findall("trafikk-og-transport", path["key"])) > 0:
                expected_themes.append(path)

        body = {
            "filters": [
                {"los": "trafikk-og-transport"},
            ],
        }
        result = post(service_url + "/search", json=body).json()
        result_themes = []
        for path in result["aggregations"]["los"]["buckets"]:
            if len(re.findall("trafikk-og-transport", path["key"])) > 0:
                result_themes.append(path)

        assert json.dumps(expected_themes) == json.dumps(result_themes)

    @pytest.mark.contract
    def test_result_should_have_theme_aggregations(self, api, wait_for_ready):
        result = post(url=service_url + "/search")
        assert "theme" in result.json()["aggregations"]

    @pytest.mark.contract
    def test_filter_on_eu_theme(self, api, wait_for_ready):
        body = {
            "filters": [
                {"theme": "GOVE"}
            ],
            "size": 100
        }
        result = post(url=service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert "theme" in hit.keys()
            id_path = parse('theme[*].code')
            assert "GOVE" in [match.value for match in id_path.find(hit)]

    @pytest.mark.contract
    def test_filter_on_eu_theme_should_handle_filters_on_multiple_themes(self, api, wait_for_ready):
        body = {
            "filters": [
                {"theme": "GOVE,ENVI"}
            ],
            "size": 100
        }

        result = post(service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert "theme" in hit.keys()
            id_path = parse('theme[*].code')
            assert "GOVE" in [match.value for match in id_path.find(hit)]
            assert "ENVI" in [match.value for match in id_path.find(hit)]

    @pytest.mark.contract
    def test_filter_on_eu_theme_ukjent(self, api, wait_for_ready):
        body = {
            "filters": [
                {"theme": "Ukjent"}
            ],
            "size": 100
        }
        result = post(service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert hit['type'] == 'dataset'
            for key in hit.keys():
                if key == "theme":
                    for entry in hit[key]:
                        assert "code" not in entry.keys()

    @pytest.mark.contract
    def test_filter_on_open_access(self, api, wait_for_ready):
        body = {
            "filters": [
                {"opendata": "true"}
            ]
        }
        result = post(url=service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0
        assert result["page"]["totalElements"] == result["aggregations"]["opendata"]["doc_count"]
        hasOpenLicenceDistribution = False
        for hits in result["hits"]:
            assert hits["accessRights"]["code"] == "PUBLIC"
            for dists in hits["distribution"]:
                if "openLicense" in dists.keys() and dists["openLicense"]:
                    hasOpenLicenceDistribution = True
                    break
        assert hasOpenLicenceDistribution is True

    @pytest.mark.contract
    def test_filter_on_unknown_access_datasets(self, api, wait_for_ready):
        body = {
            "filters": [{"accessRights": "Ukjent"}]
        }
        result = post(url=service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0
        assert result['page']['totalElements'] == result['aggregations']['accessRights']['buckets'][0]['doc_count']
        for hits in result["hits"]:
            assert "accessRights" not in hits.keys()

    @pytest.mark.contract
    def test_search_with_empty_result_should_return_empty_object(self):
        body = {
            "q": "Ainjgulu"
        }

        result = post(url=service_url + "/search", json=body).json()
        assert len(result["hits"]) == 0

    @pytest.mark.contract
    def test_specialchars_should_not_affect_result_length(self):
        body = {
            "q": "Regnskapsregisteret jm"
        }
        body_special_char = {
            "q": "Regnskapsregisteret - jm"
        }
        expected = post(url=service_url + "/search", json=body).json()["page"]["totalElements"]
        result = post(url=service_url + "/search", json=body_special_char).json()
        assert result["page"]["totalElements"] == expected


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


def has_word_in_title(hit, search_string, search_string_parts=None):
    if search_string_parts is None:
        search_string_parts = []
    if "prefLabel" in hit:
        prefLabels = hit["prefLabel"]
        prt1 = re.findall(search_string.lower(), json.dumps(prefLabels).lower())
        prt2 = 0
        if search_string_parts:
            for part in search_string_parts:
                partial_matches = re.findall(part, json.dumps(prefLabels))
                prt2 += partial_matches.__len__()
        if len(prt1) > 0 or prt2 > 0:
            return True
    elif "title" in hit:
        title = hit["title"]
        prt1 = re.findall(search_string.lower(), json.dumps(title).lower())
        if len(prt1) > 0:
            return True
    return False


def get_title_values(hit):
    """get values of all title fields for hit"""
    if "prefLabel" in hit:
        return json.dumps(hit['prefLabel'])
    elif "title" in hit:
        return json.dumps(hit['title'])
