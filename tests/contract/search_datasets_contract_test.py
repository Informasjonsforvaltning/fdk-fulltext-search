import pytest
import requests

indices_name = "datasets"
data_type = "dataset"
datasets_url = f"http://localhost:8000/{indices_name}"


class TestDataSetSearch:
    @pytest.mark.contract
    def test_response_is_ok(self, docker_service, api):
        result = requests.post(datasets_url)
        assert result.status_code == 200
