import json
import re
from datetime import datetime
import pytest
import requests
from jsonpath_ng import parse

from tests.contract.contract_utils import expected_page_keys
from tests.contract.search_all_contract_test import service_url

indices_name = "datasets"
data_type = "dataset"
datasets_url = service_url + f"/{indices_name}"


class TestDataSetSearch:

    @pytest.mark.contract
    def test_response_should_have_correct_content(self, wait_for_datasets_ready):
        result = requests.post(datasets_url)
        assert result.status_code == 200
        result_json = result.json()
        content_keys = result_json.keys()
        assert "hits" in content_keys
        result_data_types = [match.value for match in parse("hits[*].type").find(result_json["hits"])]
        for dt in result_data_types:
            assert dt == data_type
        assert "page" in content_keys
        page_key_matches = list(set(result_json["page"].keys()) & set(expected_page_keys))
        assert page_key_matches.__len__() == expected_page_keys.__len__()
        assert "aggregations" in content_keys
        aggregations = result_json["aggregations"]
        agg_keys = aggregations.keys()
        assert "los" in agg_keys
        assert len(aggregations["los"]["buckets"]) > 0
        assert "provenance" in agg_keys
        assert len(aggregations["provenance"]["buckets"]) > 0
        assert "orgPath" in agg_keys
        assert len(aggregations["orgPath"]["buckets"]) > 0
        assert "opendata" in agg_keys
        assert aggregations["opendata"]["doc_count"] > 0
        # EU-themes
        assert "theme" in agg_keys
        assert len(aggregations["theme"]["buckets"]) > 0
        assert "accessRights" in agg_keys
        assert len(aggregations["accessRights"]["buckets"]) > 0
        assert "spatial" in agg_keys
        assert len(aggregations["spatial"]["buckets"]) > 0

    @pytest.mark.contract
    def test_should_have_correct_size_and_page(self, wait_for_datasets_ready):
        result = requests.post(datasets_url)
        assert result.status_code == 200
        default_result_json = result.json()
        assert default_result_json["page"]["size"] == 10
        assert default_result_json["page"]["currentPage"] == 0
        page_request_body = {
            "page": 5
        }
        page_result = requests.post(url=datasets_url, json=page_request_body)
        assert page_result.status_code == 200
        page_result_json = page_result.json()

        assert page_result_json["page"]["size"] == 10
        assert page_result_json["page"]["currentPage"] == 5
        assert json.dumps(default_result_json["hits"][0]) != json.dumps(page_result_json["hits"][0])

    @pytest.mark.contract
    def test_should_sort_on_date(self, wait_for_datasets_ready):
        body = {
            "sorting": {"field": "harvest.firstHarvested", "direction": "desc"}
        }
        result = requests.post(url=datasets_url, json=body)
        assert result.status_code == 200
        last_date = None
        for hit in result.json()["hits"]:
            date = hit["harvest"]["firstHarvested"].split('+')[0]
            if last_date:
                assert datetime.strptime(date, "%Y-%m-%dT%H:%M:%S") <= datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%S")
            last_date = date

    @pytest.mark.contract
    def test_search_without_query_should_have_correct_sorting(self, wait_for_datasets_ready):
        """
        1. open authoritative datasets
        2. authoritative datasets
        3. open datasets
        """
        body = {
            "size": 500
        }
        result = requests.post(datasets_url)
        assert result.status_code == 200
        previous_was_open_data = True
        previous_was_authoritative = True
        for hit in result.json()["hits"]:
            if "provenance" in hit.keys():
                if hit["provenance"]["code"] == "NASJONAL":
                    assert previous_was_authoritative is True, "dataset with NASJONAL provenance encountered after " \
                                                           "non-authoritative hit"
                if hit["accessRights"]["code"] == "PUBLIC":
                    openLicence = [match.value for match in parse("distribution[*].openLicense").find(hit)]
                    if True in openLicence:
                        assert previous_was_open_data, "open authorative dataset encountered after non-open " \
                                                       "authoritative dataset dataset "
                        previous_was_open_data = True
                    else:
                        previous_was_open_data = False
                previous_was_authoritative = True
            elif hit["accessRights"]["code"] == "PUBLIC":
                assert previous_was_open_data or previous_was_authoritative, "non-authoritative open dataset, " \
                                                                             "encountered after non-open, " \
                                                                             "non authoritative dataset "
                previous_was_open_data = True
            else:
                previous_was_open_data = False
                previous_was_authoritative = False

    @pytest.mark.contract
    def test_hits_should_be_correctly_sorted_on_title(self, wait_for_datasets_ready):
        """
            1. exact match
            2. word in title
        """
        search_str = "Elbiloversikt i Norge"
        body = {
            "q": search_str,
            "size": 1000
        }
        result = requests.post(url=datasets_url, json=body)
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
    def test_should_filter_on_orgPath(self, wait_for_datasets_ready):
        org_path = "PRIVAT/910244132"
        body = {
            "filters":
                [{"orgPath": org_path}]
        }
        result = requests.post(url=datasets_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json()["hits"]
        assert len(result_json_hits) > 0
        for hit in result_json_hits:
            assert org_path in hit["publisher"]["orgPath"]

    @pytest.mark.contract
    def test_should_filter_on_spatial(self, wait_for_datasets_ready):
        expected_spatial = "Norge"
        body = {
            "filters":
                [{"spatial": expected_spatial}]

        }
        result = requests.post(url=datasets_url, json=body)
        result_json = result.json()
        assert result.status_code == 200
        assert len(result_json["hits"]) > 0
        for hit in result_json["hits"]:
            assert expected_spatial in json.dumps(hit["spatial"]["prefLabel"])

    @pytest.mark.contract
    def test_filter_on_eu_theme(self, wait_for_datasets_ready):
        body = {
            "filters": [
                {"theme": "GOVE"}
            ],
            "size": 100
        }
        result = requests.post(url=service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert "theme" in hit.keys()
            id_path = parse('theme[*].code')
            assert "GOVE" in [match.value for match in id_path.find(hit)]

    @pytest.mark.contract
    def test_filter_on_open_data(self, wait_for_datasets_ready):
        body = {
            "filters": [
                {"opendata": "true"}
            ]
        }
        result = requests.post(url=service_url + "/search", json=body).json()
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
    def test_filter_on_accessRights_NON_PUBLIC(self, wait_for_datasets_ready):
        body = {
            "filters": [{"accessRights": "NON_PUBLIC"}]
        }
        result = requests.post(url=service_url + "/search", json=body)
        for hit in result.json()["hits"]:
            assert hit["accessRights"]["code"] == "NON_PUBLIC"

    @pytest.mark.contract
    def test_should_filter_on_provenance(self, wait_for_datasets_ready):
        expected_provenance = "TREDJEPART"
        body = {
            "filters":
                [{"provenance": expected_provenance}]

        }
        result = requests.post(url=datasets_url, json=body)
        result_json = result.json()
        assert result.status_code == 200
        assert len(result_json["hits"]) > 0
        for hit in result_json["hits"]:
            assert expected_provenance in json.dumps(hit["spatial"]["prefLabel"])

    @pytest.mark.contract
    def test_should_filter_on_los(self, wait_for_datasets_ready):
        los_path = "los"
        body = {
            "filters": [{"los": los_path}]
        }
        result = requests.post(url=datasets_url, json=body)
        assert result.status_code == 200
        los_json_path = parse('themes[*].losPaths')
        for hit in result.json()["hits"]:
            assert los_path in [match.value for match in los_json_path.find(hit)]

    @pytest.mark.contract
    def test_should_filter_on_orgPath_and_spatial(self, wait_for_datasets_ready):
        expected_org_path = "PRIVAT"
        expected_spatial = "Norge"
        body = {
            "filters": [{"orgPath": expected_org_path}, {"spatial": expected_spatial}]
        }
        result = requests.post(url=datasets_url, json=body)
        assert result.status_code == 200
        result_json = result.json()
        assert len(result_json["hits"]) > 0
        for hit in result_json["hits"]:
            assert expected_org_path in hit["publisher"]["orgPath"]
            assert expected_spatial in json.dumps(hit["spatial"]["prefLabel"])

    @pytest.mark.contract
    def test_filter_on_eu_theme(self, wait_for_datasets_ready):
        body = {
            "filters": [
                {"theme": "GOVE"}
            ],
            "size": 100
        }
        result = requests.post(url=service_url + "/search", json=body).json()
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert "theme" in hit.keys()
            id_path = parse('theme[*].code')
            assert "GOVE" in [match.value for match in id_path.find(hit)]


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
