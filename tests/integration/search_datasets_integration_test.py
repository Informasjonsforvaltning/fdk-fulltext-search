from datetime import datetime
import json
import re

from flask import Flask
from jsonpath_ng import parse
import pytest

from tests.utils import expected_page_keys

indices_name = "datasets"
data_type = "dataset"
datasets_url = "/datasets"


class TestDataSetSearch:
    @pytest.mark.integration
    def test_response_should_have_correct_content(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        result = client.post(datasets_url)
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
        assert "los" in agg_keys
        assert len(aggregations["los"]["buckets"]) > 0
        assert "provenance" in agg_keys
        assert len(aggregations["provenance"]["buckets"]) > 0
        assert "orgPath" in agg_keys
        assert len(aggregations["orgPath"]["buckets"]) > 0
        assert "opendata" in agg_keys
        assert aggregations["opendata"]["doc_count"] > 0
        # EU-themes
        assert "theme" in agg_keys
        assert len(aggregations["theme"]["buckets"]) > 0
        assert "accessRights" in agg_keys
        assert len(aggregations["accessRights"]["buckets"]) > 0
        assert "spatial" in agg_keys
        assert len(aggregations["spatial"]["buckets"]) > 0
        assert "format" in agg_keys
        assert len(aggregations["format"]["buckets"]) > 0

    @pytest.mark.integration
    def test_should_have_correct_size_and_page(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        result = client.post(datasets_url)
        assert result.status_code == 200
        default_result_json = result.json
        assert default_result_json["page"]["size"] == 10
        assert default_result_json["page"]["currentPage"] == 0
        page_request_body = {"page": 5}
        page_result = client.post(datasets_url, json=page_request_body)
        assert page_result.status_code == 200
        page_result_json = page_result.json

        assert page_result_json["page"]["size"] == 10
        assert page_result_json["page"]["currentPage"] == 5
        assert json.dumps(default_result_json["hits"][0]) != json.dumps(
            page_result_json["hits"][0]
        )

    @pytest.mark.integration
    def test_should_sort_on_date(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        body = {"sorting": {"field": "harvest.firstHarvested", "direction": "desc"}}
        result = client.post(datasets_url, json=body)
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
    def test_search_without_query_should_have_correct_sorting(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        """
        1. open authoritative datasets
        2. authoritative datasets
        3. open datasets
        """
        body = {"size": 500}
        result = client.post(datasets_url, json=body)
        assert result.status_code == 200
        previous_was_open_data = True
        previous_was_authoritative = True
        for hit in result.json["hits"]:
            if "provenance" in hit.keys():
                if hit.get("provenance") and hit["provenance"]["code"] == "NASJONAL":
                    assert previous_was_authoritative is True, (
                        "dataset with NASJONAL provenance encountered after "
                        "non-authoritative hit"
                    )
                elif (
                    hit.get("accessRights") and hit["accessRights"]["code"] == "PUBLIC"
                ):
                    open_licence = [
                        match.value
                        for match in parse("distribution[*].openLicense").find(hit)
                    ]
                    if True in open_licence:
                        assert previous_was_open_data, (
                            "open authorative dataset encountered after non-open "
                            "authoritative dataset dataset "
                        )
                        previous_was_open_data = True
                    else:
                        previous_was_open_data = False
                previous_was_authoritative = True
            elif hit.get("accessRights") and hit["accessRights"]["code"] == "PUBLIC":
                assert previous_was_open_data or previous_was_authoritative, (
                    "non-authoritative open dataset, "
                    "encountered after non-open, "
                    "non authoritative dataset "
                )
                previous_was_open_data = True
            else:
                previous_was_open_data = False
                previous_was_authoritative = False

    @pytest.mark.integration
    def test_hits_should_be_correctly_sorted_on_title(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        """
        1. exact match
        2. word in title
        """
        search_str = "Elbiloversikt i Norge"
        body = {"q": search_str, "size": 1000}
        result = client.post(datasets_url, json=body)
        assert result.status_code == 200
        result_json = result.json
        last_was_exact_match = True
        last_was_partial_match_in_title = False
        for hit in result_json["hits"]:
            if has_exact_match_in_title(hit, search_str):
                assert last_was_exact_match
                last_was_exact_match = True
            elif has_partial_match_in_title(hit, search_str):
                assert last_was_exact_match or last_was_partial_match_in_title
                last_was_exact_match = False
                last_was_partial_match_in_title = True
            else:
                last_was_exact_match = False
                last_was_partial_match_in_title = False

    @pytest.mark.integration
    def test_should_filter_on_org_path(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        org_path = "/STAT/972417858/971040238"
        body = {"filters": [{"orgPath": org_path}]}
        result = client.post(datasets_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json["hits"]
        assert len(result_json_hits) > 0
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
                        "values": ["UNKNOWN"],
                    }
                }
            ]
        }
        result = client.post(datasets_url, json=body)
        assert result.status_code == 200
        result_json_hits = result.json["hits"]
        assert len(result_json_hits) == 10
        for hit in result_json_hits:
            fdk_formats = []
            if hit["distribution"] is not None:
                for distr in hit["distribution"]:
                    if distr["fdkFormat"] is not None:
                        fdk_formats.extend(distr["fdkFormat"])
            assert any(f["type"] == "UNKNOWN" for f in fdk_formats)

    @pytest.mark.integration
    def test_should_filter_on_spatial(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        expected_spatial = "Norge"
        body = {"filters": [{"spatial": expected_spatial}]}
        result = client.post(datasets_url, json=body)
        result_json = result.json
        assert result.status_code == 200
        assert len(result_json["hits"]) > 0
        for hit in result_json["hits"]:
            spatial_path_nb = parse("spatial[*].prefLabel.nb")
            spatial_path_no = parse("spatial[*].prefLabel.no")
            assert expected_spatial in [
                match.value for match in spatial_path_nb.find(hit)
            ] or expected_spatial in [
                match.value for match in spatial_path_no.find(hit)
            ]

    @pytest.mark.integration
    def test_filter_on_eu_theme(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        body = {"filters": [{"theme": "GOVE"}], "size": 100}
        result = client.post("/search", json=body).json
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert "theme" in hit.keys()
            id_path = parse("theme[*].code")
            assert "GOVE" in [match.value for match in id_path.find(hit)]

    @pytest.mark.integration
    def test_filter_on_open_data(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        body = {"filters": [{"opendata": "true"}]}
        result = client.post("/search", json=body).json
        assert len(result["hits"]) > 0
        assert (
            result["page"]["totalElements"]
            == result["aggregations"]["opendata"]["doc_count"]
        )
        has_open_licence_distribution = False
        for hits in result["hits"]:
            assert hits["accessRights"]["code"] == "PUBLIC"
            for dists in hits["distribution"]:
                if "openLicense" in dists.keys() and dists["openLicense"]:
                    has_open_licence_distribution = True
                    break
        assert has_open_licence_distribution is True

    @pytest.mark.integration
    def test_filter_on_access_rights_non_public(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        body = {"filters": [{"accessRights": "NON_PUBLIC"}]}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            assert hit["accessRights"]["code"] == "NON_PUBLIC"

    @pytest.mark.integration
    def test_should_filter_on_provenance(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        expected_provenance = "TREDJEPART"
        body = {"filters": [{"provenance": expected_provenance}]}
        result = client.post(datasets_url, json=body)
        result_json = result.json
        assert result.status_code == 200
        assert len(result_json["hits"]) > 0
        for hit in result_json["hits"]:
            provenance_path = parse("provenance.code")
            assert expected_provenance in [
                match.value for match in provenance_path.find(hit)
            ]

    @pytest.mark.integration
    def test_should_filter_on_los(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        los_path = "bygg-og-eiendom"
        body = {"filters": [{"los": los_path}]}
        result = client.post(datasets_url, json=body)
        assert result.status_code == 200
        result_hits = result.json["hits"]
        assert len(result_hits) > 0
        for hit in result_hits:
            los_paths = ",".join(
                [",".join(los_theme["losPaths"]) for los_theme in hit["losTheme"]]
            )
            assert los_path in los_paths

    @pytest.mark.integration
    def test_should_filter_on_org_path_and_spatial(
        self, client: Flask, docker_service, api, wait_for_datasets_ready
    ):
        expected_org_path = "/ANNET"
        expected_spatial = "Norge"
        body = {"filters": [{"orgPath": "/ANNET"}, {"spatial": "Norge"}]}
        result = client.post(datasets_url, json=body)
        assert result.status_code == 200
        result_json = result.json
        assert len(result_json["hits"]) > 0
        for hit in result_json["hits"]:
            assert expected_org_path in hit["publisher"]["orgPath"]
            spatial_nb_path = parse("spatial[*].prefLabel.nb")
            spatial_no_path = parse("spatial[*].prefLabel.no")
            has_correct_spatial = expected_spatial in [
                match.value for match in spatial_nb_path.find(hit)
            ] or expected_spatial in [
                match.value for match in spatial_no_path.find(hit)
            ]
            assert has_correct_spatial

    @pytest.mark.integration
    def test_filter_with_transport_profile(
        self, client: Flask, wait_for_datasets_ready
    ):

        default_profile_body = {
            "filters": [
                {"accessRights": "PUBLIC"},
                {
                    "los": "trafikk-og-transport/mobilitetstilbud,trafikk-og-transport/trafikkinformasjon,"
                    "trafikk-og-transport/veg-og-vegregulering,trafikk-og-transport/yrkestransport"
                },
            ]
        }

        default_profile_result = client.post("/datasets", json=default_profile_body)
        transport_profile_body = {
            "filters": [{"accessRights": "PUBLIC"}, {"themeprofile": "transport"}]
        }
        transport_profile_result = client.post("/datasets", json=transport_profile_body)
        assert transport_profile_result.status_code == 200
        assert len(transport_profile_result.json["hits"]) > len(
            default_profile_result.json["hits"]
        )

        los_key_1 = "trafikk-og-transport/mobilitetstilbud"
        los_key_2 = "trafikk-og-transport/trafikkinformasjon"
        los_key_3 = "trafikk-og-transport/veg-og-vegregulering"
        los_key_4 = "trafikk-og-transport/yrkestransport"
        partial_hits = 0
        for hit in transport_profile_result.json["hits"]:
            los_key_path = parse("losTheme[*].losPaths[*]")
            los_keys = [match.value for match in los_key_path.find(hit)]
            matches = union_los_lists(
                los_keys, [los_key_1, los_key_2, los_key_3, los_key_4]
            )
            if matches.__len__() == 4:
                pass
            elif matches.__len__() > 0:
                partial_hits += 1
            else:
                raise AssertionError("no occurrence of los themes for profile")
        assert partial_hits > 0


def union_los_lists(result_list: list, expected_list: list):
    union = []
    result_str = " ".join(result_list)
    for path in expected_list:
        if re.findall(path, result_str).__len__() > 0:
            union.append(path)
    return union


def has_exact_match_in_title(hit, search_str):
    title = hit["title"]
    keys = title.keys()
    has_exact_match = False
    if "nb" in keys and title["nb"] == search_str:
        has_exact_match = True
    if "nn" in keys and title["nn"] == search_str:
        has_exact_match = True
    if "no" in keys and title["no"] == search_str:
        has_exact_match = True
    if "en" in keys and title["en"] == search_str:
        has_exact_match = True
    return has_exact_match


def has_partial_match_in_title(hit, search_str):
    title = hit["title"]
    prt1 = re.findall(search_str.lower(), json.dumps(title).lower())
    if len(prt1) > 0:
        return True
    else:
        return False


def get_time(timestamp: str):
    return datetime.strptime(timestamp.split("T")[0], "%Y-%M-%d")
