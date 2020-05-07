import time

import pytest
import requests
from requests import get
from urllib3.exceptions import MaxRetryError, NewConnectionError


@pytest.fixture(scope="function")
def wait_for_information_models():
    timeout = time.time() + 90
    try:
        while True:
            response = get("http://localhost:8000/indices?name=informationmodels")
            if response.json()[0]['count'] >= 530:
                break
            if time.time() > timeout:
                pytest.fail(
                    'Test function setup: timed out while waiting for fulltext-search, last response '
                    'was {0}'.format(response.json()["count"]))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test function setup: could not contact fdk-fulltext-search container')
    yield


class TestInformationModelSearch:

    @pytest.mark.contract
    def test_response_should_have_correct_content(api, wait_for_information_models):
        print("yei!")
