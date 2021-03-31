import json
import re

from flask import Flask
import pytest

suggestions_endpoint = "/suggestion"


class TestSuggestions:
    @pytest.mark.integration
    def test_suggestion_not_implemented(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        result = client.get(suggestions_endpoint)
        assert result.status_code == 501

    @pytest.mark.integration
    def test_suggestion_bad_request(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        result = client.get(suggestions_endpoint + "/invalid")
        assert result.status_code == 400

    @pytest.mark.integration
    def test_suggestion_datasets(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        prefix = "Statisti"
        result = client.get(f"{suggestions_endpoint}/datasets?q={prefix}")
        assert result.status_code == 200
        previous_was_prefix = True
        was_prefix_count = 0
        was_partial_count = 0
        for hit in result.json["suggestions"]:
            if has_prefix_in_title_all_languages(hit["title"], prefix):
                assert (
                    previous_was_prefix
                ), "Prefix match encountered after other suggestions"
                was_prefix_count += 1
            else:
                assert has_partial_match_in_title(
                    hit["title"], prefix
                ), "Title without match on prefix encountered "
                was_partial_count += 1
        assert was_prefix_count > 0
        assert was_partial_count > 0

    @pytest.mark.integration
    def test_suggestion_concepts(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        prefix = "Dokume"
        result = client.get(f"{suggestions_endpoint}/concepts?q={prefix}")
        assert result.status_code == 200
        previous_was_prefix = True
        was_prefix_count = 0
        was_partial_count = 0
        for hit in result.json["suggestions"]:
            if has_prefix_in_title_all_languages(hit["prefLabel"], prefix):
                assert (
                    previous_was_prefix
                ), "Prefix match encountered after other suggestions"
                was_prefix_count += 1
            else:
                assert has_partial_match_in_title(
                    hit["prefLabel"], prefix
                ), "Title without match on prefix encountered "
                was_partial_count += 1

    @pytest.mark.integration
    def test_suggestion_dataservices(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        prefix = "Swag"
        result = client.get(f"{suggestions_endpoint}/dataservices?q={prefix}")
        assert result.status_code == 200
        assert len(result.json["suggestions"]) > 0
        previous_was_prefix = True
        was_prefix_count = 0
        was_partial_count = 0
        for hit in result.json["suggestions"]:
            if has_prefix_in_title_all_languages(hit["title"], prefix):
                assert (
                    previous_was_prefix
                ), "Prefix match encountered after other suggestions"
                was_prefix_count += 1
            else:
                assert has_partial_match_in_title(
                    hit["title"], prefix
                ), "Title without match on prefix encountered "
                was_partial_count += 1

    @pytest.mark.integration
    def test_suggestion_information_models(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        prefix = "div"
        result = client.get(f"{suggestions_endpoint}/informationmodels?q={prefix}")
        assert result.status_code == 200
        assert len(result.json["suggestions"]) > 0
        previous_was_prefix = True
        was_prefix_count = 0
        was_partial_count = 0
        for hit in result.json["suggestions"]:
            if has_prefix_in_title_all_languages(hit["title"], prefix):
                assert (
                    previous_was_prefix
                ), "Prefix match encountered after other suggestions"
                was_prefix_count += 1
            else:
                assert has_partial_match_in_title(
                    hit["title"], prefix
                ), "Title without match on prefix encountered "
                was_partial_count += 1


def has_prefix_in_title_all_languages(title, prefix):
    keys = title.keys()
    has_match_in_prefix = False
    if "nb" in keys and title["nb"].startswith(prefix):
        has_match_in_prefix = True
    if "nn" in keys and title["nb"].startswith(prefix):
        has_match_in_prefix = True
    if "no" in keys and title["nb"].startswith(prefix):
        has_match_in_prefix = True
    if "en" in keys and title["nb"].startswith(prefix):
        has_match_in_prefix = True
    return has_match_in_prefix


def has_partial_match_in_title(title, prefix):
    prt1 = re.findall(prefix.lower(), json.dumps(title).lower())
    if len(prt1) > 0:
        return True
    else:
        return False
