import pytest
import requests

from tests.contract.search_all_contract_test import service_url

indices_name = ["dataservices", "datasets", "concepts", "informationmodels"]

index_url = service_url + "/indices"


class TestSearchAll:
    @pytest.mark.contract
    def test_should_return_status_of_all_indices(self, api):
        result = requests.get(index_url)
        assert result.status_code == 200
        count = 0
        for index in result.json():
            keys = index.keys()
            assert index['name'] in indices_name
            assert "lastUpdate" in keys
            assert "count" in keys
            assert isinstance(index["count"], int)
            count += 1
        assert count == 4

    @pytest.mark.contract
    def test_should_return_status_of_concept_index(self, api):
        result = requests.get(index_url + "?name=concepts")
        assert result.status_code == 200
        assert result.json()[0]['name'] == 'concepts'
        keys = result.json()[0].keys()
        assert "lastUpdate" in keys
        assert "count" in keys
        assert isinstance(result.json()[0]["count"], int)

    @pytest.mark.contract
    def test_should_return_404_for_unkown_index_names(self, api):
        result = requests.get(index_url + "?name=nonsens")
        assert result.status_code == 400

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
