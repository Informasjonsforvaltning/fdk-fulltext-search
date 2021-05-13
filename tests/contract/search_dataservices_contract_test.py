import pytest
import requests

indices_name = "dataservices"
data_type = "dataservice"
data_services_url = f"http://localhost:8000/{indices_name}"


class TestDataServiceSearch:
    @pytest.mark.contract
    def test_response_is_ok(self, docker_service, api):
        result = requests.post(data_services_url)
        assert result.status_code == 200
