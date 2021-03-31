import json
import re

from flask import Flask
from jsonpath_ng import parse
import pytest

from tests.utils import expected_page_keys

indices_name = "concepts"
data_type = "concept"
concept_url = "/concepts"


class TestConceptSearch:
    @pytest.mark.integration
    def test_response_should_have_correct_content(
        self, client: Flask, docker_service, api, wait_for_concepts
    ):
        result = client.post(concept_url)
        result_json = result.json
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

    @pytest.mark.integration
    def test_hits_should_be_correctly_sorted_on_title(
        self, client: Flask, docker_service, api, wait_for_concepts
    ):
        """
        1. exact match
        2. word in title
        """
        search_str = "skattefri inntekt"
        body = {"q": search_str, "size": 300}
        result = client.post(concept_url, json=body)
        assert result.status_code == 200
        result_json = result.json
        exact_match_exists = False
        last_was_exact_match = True
        last_was_partial_match_in_title = False
        for hit in result_json["hits"]:
            if has_exact_match_in_title(hit, search_str):
                assert last_was_exact_match
                last_was_exact_match = True
                exact_match_exists = True
            elif has_partial_match_in_title(hit, search_str):
                assert last_was_exact_match or last_was_partial_match_in_title
                last_was_exact_match = False
                last_was_partial_match_in_title = True
            else:
                last_was_exact_match = False
                last_was_partial_match_in_title = False

        assert exact_match_exists

    @pytest.mark.integration
    def test_should_filter_on_org_path(
        self, client: Flask, docker_service, api, wait_for_concepts
    ):
        org_path = "/STAT/972417807/974761076"
        body = {"filters": [{"orgPath": org_path}]}
        result = client.post(concept_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json["hits"]
        assert len(result_json_hits) > 0
        for hit in result_json_hits:
            assert org_path in hit["publisher"]["orgPath"]

    @pytest.mark.integration
    def test_should_have_correct_size_and_page(
        self, client: Flask, docker_service, api, wait_for_concepts
    ):
        default_result = client.post(concept_url).json
        assert default_result["page"]["size"] == 10
        assert default_result["page"]["currentPage"] == 0

        page_request_body = {"page": 5}
        page_result = client.post(concept_url, json=page_request_body).json
        assert page_result["page"]["size"] == 10
        assert page_result["page"]["currentPage"] == 5

        assert json.dumps(default_result["hits"][0]) != json.dumps(
            page_result["hits"][0]
        )


def has_exact_match_in_title(hit, search_str):
    title = hit["prefLabel"]
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
    title = hit["prefLabel"]
    prt1 = re.findall(search_str.lower(), json.dumps(title).lower())
    if len(prt1) > 0:
        return True
    else:
        return False
