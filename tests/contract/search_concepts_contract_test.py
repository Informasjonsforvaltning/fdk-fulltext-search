import pytest
import requests

indices_name = "concepts"
data_type = "concept"
concept_url = f"http://localhost:8000/{indices_name}"


class TestConceptSearch:
    @pytest.mark.contract
    def test_response_is_ok(self, docker_service, api):
        result = requests.post(concept_url)
        assert result.status_code == 200
