from datetime import datetime
import json

from flask import Flask
from jsonpath_ng import parse
import pytest

from tests.utils import expected_page_keys

indices_name = "dataservices"
data_type = "dataservice"
data_services_url = "/dataservices"


class TestDataServiceSearch:
    @pytest.mark.integration
    def test_response_should_have_correct_content(
        self, client: Flask, docker_service, api, wait_for_dataservice_ready
    ):
        result = client.post(data_services_url)
        assert result.status_code == 200
        result_json = result.json
        content_keys = result_json.keys()
        assert "hits" in content_keys
        result_data_types = [
            match.value for match in parse("hits[*].type").find(result_json["hits"])
        ]
        for dt in result_data_types:
            assert dt == data_type
        assert "page" in content_keys
        page_key_matches = list(
            set(result_json["page"].keys()) & set(expected_page_keys)
        )
        assert page_key_matches.__len__() == expected_page_keys.__len__()
        assert "aggregations" in content_keys
        aggregations = result_json["aggregations"]
        agg_keys = aggregations.keys()
        assert "orgPath" in agg_keys
        assert len(aggregations["orgPath"]["buckets"]) > 0
        assert "format" in agg_keys
        assert len(aggregations["format"]["buckets"]) > 0

    @pytest.mark.integration
    def test_should_have_correct_size_and_page(
        self, client: Flask, docker_service, api, wait_for_dataservice_ready
    ):
        result = client.post(data_services_url)
        assert result.status_code == 200
        default_result_json = result.json
        assert default_result_json["page"]["size"] == 10
        assert default_result_json["page"]["currentPage"] == 0
        page_request_body = {"page": 1}
        page_result = client.post(data_services_url, json=page_request_body)
        assert page_result.status_code == 200
        page_result_json = page_result.json

        assert page_result_json["page"]["size"] == 3
        assert page_result_json["page"]["currentPage"] == 1
        assert json.dumps(default_result_json["hits"][0]) != json.dumps(
            page_result_json["hits"][0]
        )

    @pytest.mark.integration
    def test_should_sort_on_date(
        self, client: Flask, docker_service, api, wait_for_dataservice_ready
    ):
        body = {"sorting": {"field": "harvest.firstHarvested", "direction": "desc"}}
        result = client.post(data_services_url, json=body)
        assert result.status_code == 200
        last_date = None
        for hit in result.json["hits"]:
            date = hit["harvest"]["firstHarvested"].split("+")[0]
            if last_date:
                assert datetime.strptime(
                    date, "%Y-%m-%dT%H:%M:%SZ"
                ) <= datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%SZ")
            last_date = date

    @pytest.mark.integration
    def test_should_filter_on_org_path(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        org_path = "PRIVAT/910244132"
        body = {"filters": [{"orgPath": org_path}]}
        result = client.post(data_services_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json["hits"]
        assert len(result_json_hits) == 5
        for hit in result_json_hits:
            assert org_path in hit["publisher"]["orgPath"]

    @pytest.mark.integration
    def test_should_filter_on_fdk_format(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        body = {
            "filters": [
                {
                    "collection": {
                        "field": "fdkFormatPrefixed.keyword",
                        "values": ["MEDIA_TYPE application/rdf+xml"],
                    }
                }
            ]
        }
        result = client.post(data_services_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json["hits"]
        assert len(result_json_hits) == 3
        assert any(
            "application/rdf+xml" == hit["fdkFormat"][0]["code"]
            for hit in result_json_hits
        )

    @pytest.mark.integration
    def test_get_single_data_service_with_id_search(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        body = {"filters": [{"_id": "d1d698ef-267a-3d57-949f-b2bc44657f3e"}]}
        result = client.post(data_services_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json["hits"]
        assert len(result_json_hits) == 1
        assert result_json_hits[0].get("id") == "d1d698ef-267a-3d57-949f-b2bc44657f3e"


def get_time(timestamp: str):
    return datetime.strptime(timestamp.split("T")[0], "%Y-%M-%d")
