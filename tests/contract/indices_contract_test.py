import pytest
import requests

from tests.contract.search_contract_test import service_url

indices_name = ["dataservices", "datasets", "concepts", "informationmodels"]

index_url = service_url + "/indices"


class TestSearchAll:
    @pytest.mark.contract
    def test_should_return_status_of_all_indices(self, api):
        result = requests.get(index_url)
        assert result.status_code == 200
        count = 0
        for index in result.json():
            assert index['name'] in indices_name
            count += 1
        assert count == 4

    @pytest.mark.contract
    def test_should_return_status_of_all_concept_index(self, api):
        result = requests.get(index_url + "?name=concepts")
        assert result.status_code == 200
        assert result.json()[0]['name'] == 'concepts'

    @pytest.mark.contract
    def test_should_return_status_of_all_concept_index(self, api):
        result = requests.get(index_url + "?name=nonsens")
        assert result.status_code == 400

    @pytest.mark.contract
    def test_should_reindex_all_indices(self, api):
        last_updates = requests.get(url=index_url).json()
        result = requests.post(url=index_url)
        assert result.status_code == 201
        assert result.json()['status'] == "OK"
        new_updates = requests.get(url=index_url).json()
        for i in range(0, len(last_updates)):
            assert new_updates[i]['lastUpdate'] > last_updates[i]["lastUpdate"]

    @pytest.mark.contract
    def test_should_update_dataset_index(self, api):
        last_update = requests.get(url=index_url + "?name=datasets").json()
        result = requests.post(url=index_url + "?name=datasets")
        assert result.status_code == 201
        new_update = requests.get(url=index_url + "?name=datasets").json()
        assert new_update[0]['lastUpdate'] > last_update[0]["lastUpdate"]

    @pytest.mark.contract
    def test_should_return_400_response(self, api):
        result = requests.post(url=index_url + "?name=nope")
        assert result.status_code == 400