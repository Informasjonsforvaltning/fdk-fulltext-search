import time

import pytest
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError

from tests.contract.search_contract_test import service_url

indices_name = ["dataservices", "datasets", "concepts", "informationmodels"]

es_dataservice_url = "http://localhost:9200/dataservices"


@pytest.fixture(scope="function")
def wait_for_dataservice_ready():
    timeout = time.time() + 90
    try:
        while True:
            response = requests.get(es_dataservice_url + "/_count")
            if response.json()['count'] >= 126:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for poupulation of ElasticSearch, last response '
                    'was {0}'.format(response.json()["count"]))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test function setup: could not contact elasticsearch container')
    yield


class TestMapping:
    @pytest.mark.contract
    def test_json_in_apiSpecification_should_not_be_indexed(self, wait_for_dataservice_ready):
        result_mapping = requests.get(es_dataservice_url + "/_mapping")
        api_spec_mapping = result_mapping.json()["dataservices"]["mappings"]["properties"]["apiSpecification"].keys()
        assert len(api_spec_mapping) == 2
        assert "type" in api_spec_mapping
        assert "enabled" in api_spec_mapping

