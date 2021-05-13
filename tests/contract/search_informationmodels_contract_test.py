import pytest
import requests

indices_name = "informationmodels"
data_type = "informationmodel"
informationmodel_url = f"http://localhost:8000/{indices_name}"


class TestInformationModelSearch:
    @pytest.mark.contract
    def test_response_is_ok(self, docker_service, api):
        result = requests.post(informationmodel_url)
        assert result.status_code == 200
