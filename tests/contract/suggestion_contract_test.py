import pytest
import requests

suggestions_endpoint = "http://localhost:8000/suggestion"


class TestSuggestions:
    @pytest.mark.contract
    def test_suggestion_not_implemented(self, docker_service, api):
        result = requests.get(suggestions_endpoint)
        assert result.status_code == 501

    @pytest.mark.contract
    def test_suggestion_bad_request(self, docker_service, api):
        result = requests.get(suggestions_endpoint + "/invalid")
        assert result.status_code == 400

    @pytest.mark.contract
    def test_suggestion_datasets_is_implemented(self, docker_service, api):
        prefix = "Statisti"
        result = requests.get(f"{suggestions_endpoint}/datasets?q={prefix}")
        assert result.status_code == 200

    @pytest.mark.contract
    def test_suggestion_concepts_is_implemented(self, docker_service, api):
        prefix = "Dokume"
        result = requests.get(f"{suggestions_endpoint}/concepts?q={prefix}")
        assert result.status_code == 200

    @pytest.mark.contract
    def test_suggestion_dataservices_is_implemented(self, docker_service, api):
        prefix = "Swag"
        result = requests.get(f"{suggestions_endpoint}/dataservices?q={prefix}")
        assert result.status_code == 200

    @pytest.mark.contract
    def test_suggestion_information_models_is_implemented(self, docker_service, api):
        prefix = "div"
        result = requests.get(f"{suggestions_endpoint}/informationmodels?q={prefix}")
        assert result.status_code == 200
