import json
import re

import pytest
import requests

from tests.contract.search_all_contract_test import service_url

suggestions_endpoint = service_url + '/suggestion'


class TestSuggestions:
    @pytest.mark.contract
    def test_suggestion_not_implemented(self, wait_for_ready):
        result = requests.get(suggestions_endpoint)
        assert result.status_code == 501
        result_info_models = requests.get(suggestions_endpoint + '/informationmodels')
        assert result_info_models.status_code == 501
        result_dataservices = requests.get(suggestions_endpoint + '/dataservices')
        assert result_dataservices.status_code == 501
        result_concepts_models = requests.get(suggestions_endpoint + '/concepts')
        assert result_concepts_models.status_code == 501

    @pytest.mark.contract
    def test_suggestion_bad_request(self, wait_for_ready):
        result = requests.get(suggestions_endpoint + '/invalid')
        assert result.status_code == 400

    @pytest.mark.contract
    def test_suggestion_datasets(self, wait_for_datasets_ready):
        prefix = "Statisti"
        result = requests.get(suggestions_endpoint + '/datasets?q='.format(prefix))
        assert result.status_code == 200
        previous_was_prefix = True
        was_prefix_count = 0
        was_partial_count = 0
        for suggestion in result.json():
            if has_prefix_in_title_all_languages(suggestion, prefix):
                assert previous_was_prefix, "Prefix match encountered after other suggestions"
                was_prefix_count += 1
            else:
                assert has_partial_match_in_title(suggestion, prefix), "Title without match on prefix encountered "
                was_partial_count += 1
        assert was_prefix_count > 0
        assert was_partial_count > 0


def has_prefix_in_title_all_languages(suggestion, prefix):
    title = suggestion["title"]
    keys = title.keys()
    has_match_in_prefix = False
    if "nb" in keys and title["nb"].startsWith(prefix):
        has_match_in_prefix = True
    if "nn" in keys and title["nb"].startsWith(prefix):
        has_match_in_prefix = True
    if "no" in keys and title["nb"].startsWith(prefix):
        has_match_in_prefix = True
    if "en" in keys and title["nb"].startsWith(prefix):
        has_match_in_prefix = True
    return has_match_in_prefix


def has_partial_match_in_title(suggestion, prefix):
    title = suggestion["title"]
    prt1 = re.findall(prefix.lower(), json.dumps(title).lower())
    if len(prt1) > 0:
        return True
    else:
        return False
