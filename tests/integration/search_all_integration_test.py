from datetime import datetime
import json
import re
from typing import Dict, List, Optional

from flask import Flask
from jsonpath_ng import parse
import pytest

data_types = ["dataservice", "dataset", "concept", "informationmodel"]


class TestSearchAll:
    @pytest.mark.integration
    def test_search_without_body_should_return_response_with_hits_aggregations_and_page(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        result = client.post("/search").json
        has_hits = False
        has_aggregation = False
        has_page = False
        unknown_items = []
        for k, _v in result.items():
            if k == "hits":
                has_hits = True
            elif k == "aggregations":
                has_aggregation = True
            elif k == "page":
                has_page = True
            else:
                unknown_items.append(k)
        assert has_hits is True
        assert has_aggregation is True
        assert has_page is True
        assert len(unknown_items) == 0

    @pytest.mark.integration
    def test_search_without_query_should_have_correct_sorting(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        """
        1. open authoritative datasets
        2. authoritative datasets
        3. authoritative dataservices
        """
        opts = {"size": 200}
        result = client.post("/search", json=opts).json["hits"]

        assert len(result) > 0
        debug_values: Dict = {"authority": [], "previous_dataset": [], "datatype": []}
        previous_was_dataset = True
        previous_was_open_data = True
        previous_was_authority = True
        for hits in result:
            if hits.get("nationalComponent"):
                if hits["nationalComponent"]:
                    assert previous_was_authority is True, (
                        "nationalCompoent dataservice encountered after "
                        "non-authoritative hit {0}".format(json.dumps(debug_values))
                    )
                    previous_was_authority = True
                else:
                    previous_was_authority = False
            elif hits.get("provenance"):
                if hits["provenance"]["code"] == "NASJONAL":
                    assert previous_was_dataset is True, (
                        "dataset with NASJONAL provenance encountered after other "
                        "data types {0}".format(json.dumps(debug_values))
                    )
                    assert previous_was_authority is True, (
                        "dataset with NASJONAL provenance encountered after "
                        "non-authoritative hit {0}".format(json.dumps(debug_values))
                    )
                    if hits["accessRights"]["code"] == "PUBLIC":
                        open_licence = [
                            match.value
                            for match in parse("distribution[*].openLicense").find(hits)
                        ]
                        if True in open_licence:
                            assert (
                                previous_was_open_data
                            ), "open dataset encountered after non-open dataset dataset"
                            previous_was_open_data = True
                        else:
                            previous_was_open_data = False
                    previous_was_authority = True
                else:
                    previous_was_authority = False
            else:
                previous_was_authority = False
            previous_was_dataset = hits["type"] == "dataset"
            debug_values["authority"].append(previous_was_authority)
            debug_values["previous_dataset"].append(previous_was_dataset)
            debug_values["datatype"].append(hits["type"])

    @pytest.mark.integration
    def test_search_without_body_should_contain_default_aggs(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        result = client.post("/search").json["aggregations"]
        keys = result.keys()
        assert "los" in keys
        assert "orgPath" in keys
        assert "availability" in keys
        assert "accessRights" in keys
        assert "opendata" in keys
        assert "theme" in keys
        assert len(result["los"]["buckets"]) > 0
        assert len(result["orgPath"]["buckets"]) > 0
        assert len(result["availability"]["buckets"]) == 3
        assert len(result["accessRights"]["buckets"]) > 0
        assert len(result["theme"]["buckets"]) > 0

    @pytest.mark.integration
    def test_all_hits_should_have_type(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        result = client.post("/search").json["hits"]
        for hit in result:
            assert "type" in hit.keys()
            assert hit["type"] in data_types

    @pytest.mark.integration
    def test_hits_should_have_object_without_es_data(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        result = client.post("/search").json["hits"]
        for hit in result:
            assert "_type" not in hit.keys()
            assert "_source" not in hit.keys()

    @pytest.mark.integration
    def test_hits_should_start_with_exact_matches_in_title(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        srch_string = "dokument"
        body = {"q": "dokument", "size": 1000}
        last_was_exact = True
        exact_matches = 0
        position = 0
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            if "prefLabel" in hit:
                pref_labels = hit["prefLabel"]
                if is_exact_match(pref_labels.keys(), pref_labels, srch_string):
                    assert last_was_exact, "exact match found at position {0}".format(
                        position
                    )
                    exact_matches += 1
                else:
                    last_was_exact = False
            elif "title" in hit:
                title = hit["title"]
                if isinstance(title, dict):
                    if is_exact_match(title.keys(), title, srch_string):
                        assert (
                            last_was_exact
                        ), "exact match found at position {0}".format(position)
                        exact_matches += 1
                    else:
                        last_was_exact = False
                else:
                    if title.lower() == srch_string:
                        assert (
                            last_was_exact
                        ), "exact match found at position {0}".format(position)
                        exact_matches += 1
                    else:
                        last_was_exact = False
            position += 1
        assert exact_matches > 0

    @pytest.mark.integration
    def test_hits_should_have_hit_in_owner_before_hit_in_description(
        self, client: Flask, wait_for_ready
    ):
        search_string = "Statens vegvesen"
        body = {"q": search_string, "size": 1000}
        result = client.post("/search", json=body)
        match_in_description = False
        match_on_publisher_name = False
        for hit in result.json["hits"]:
            match_str = search_string.lower()
            title = get_title_values(hit)
            if match_str == hit.get("publisher").get("name"):
                match_on_publisher_name = True
                assert match_in_description is False
            elif hit.get("publisher").get("prefLabel"):
                publisher_labels = hit.get("publisher").get("prefLabel")
                for key in publisher_labels.keys():
                    if publisher_labels[key] == search_string:
                        match_on_publisher_name = True
                        assert match_in_description is False
            elif re.findall(get_matches_with_stemming_regex(match_str), title.lower()):
                continue
            elif is_match_in_descriptive_texts(search_string, hit):
                match_in_description = True
        if match_in_description:
            assert match_on_publisher_name

    @pytest.mark.integration
    def test_hits_should_contain_search_string(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"q": "barnehage"}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            values = json.dumps(hit)
            prt1 = re.findall("barnehage", values)
            prt2 = re.findall("Barnehage", values)
            arr = prt1 + prt2
            assert (len(arr)) > 0

    @pytest.mark.integration
    def test_search_on_several_words_should_include_partial_matches_in_title(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        search_str = "Test for los"
        body = {"q": search_str, "size": "100"}
        result = client.post("/search", json=body).json
        assert result["page"]["totalElements"] > 1
        data_type_count = {
            "dataservice": 0,
            "dataset": 0,
            "informationmodel": 0,
            "concept": 0,
        }
        match_type_count = {"complete": 0, "one_word": 0, "two_words": 0}

        for hit in result["hits"]:
            data_type = hit["type"]
            data_type_count[data_type] += 1
            words_in_title = re.findall(r"\w+", get_title_values(hit).lower())
            matches = list(
                set(words_in_title) & set(search_str.lower().split())
            ).__len__()
            if matches == 3:
                match_type_count["complete"] += 1
            elif matches == 2:
                match_type_count["two_words"] += 1
            elif matches == 1:
                match_type_count["one_word"] += 1

        assert match_type_count["one_word"] > 0, "No one word matches for {0}".format(
            search_str
        )
        assert match_type_count["two_words"] > 0, "No two word matches for {0}".format(
            search_str
        )

    @pytest.mark.integration
    def test_hits_should_be_filtered_on_org_path(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"orgPath": "/PRIVAT"}]}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            assert "PRIVAT" in hit["publisher"]["orgPath"]

    @pytest.mark.integration
    def test_hits_should_have_word_and_be_filtered_on_org_path(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"q": "barnehage", "filters": [{"orgPath": "/KOMMUNE/840029212"}]}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            values = json.dumps(hit)
            prt1 = re.findall("barnehage", values)
            prt2 = re.findall("Barnehage", values)
            arr = prt1 + prt2
            assert (len(arr)) > 0
            assert "/KOMMUNE/840029212" in hit["publisher"]["orgPath"]

    @pytest.mark.integration
    def test_hits_should_be_filtered_on_is_open_access(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"isOpenAccess": "true"}]}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            assert hit["isOpenAccess"] is True

    @pytest.mark.integration
    def test_hits_should_have_word_and_be_filtered_on_is_not_open_access(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"isOpenAccess": "false"}]}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            assert hit["isOpenAccess"] is False

    @pytest.mark.integration
    def test_hits_should_be_filtered_on_access_rights_public(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"accessRights": "PUBLIC"}]}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            assert hit["accessRights"]["code"] == "PUBLIC"

    @pytest.mark.integration
    def test_hits_should_be_filtered_on_access_rights_non_public(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"accessRights": "NON_PUBLIC"}]}
        result = client.post("/search", json=body)
        for hit in result.json["hits"]:
            assert hit["accessRights"]["code"] == "NON_PUBLIC"

    @pytest.mark.integration
    def test_empty_request_after_request_with_q_should_return_default(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"q": "barn"}
        client.post("/search", json=body)
        client.post("/search", json=body)
        client.post("/search", json=body)
        pre_request = client.post("/search", json=body)
        result = client.post("/search")
        assert json.dumps(pre_request.json) != json.dumps(result.json)

    @pytest.mark.integration
    def test_sort_should_returns_the_most_recent_hits(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"sorting": {"field": "harvest.firstHarvested", "direction": "desc"}}
        result = client.post("/search", json=body)
        last_date = None
        for hit in result.json["hits"]:
            assert "harvest" in hit
            current_date = datetime.strptime(
                hit["harvest"]["firstHarvested"].split("T")[0], "%Y-%m-%d"
            )
            if last_date is not None:
                assert current_date <= last_date
            last_date = current_date

    @pytest.mark.integration
    def test_sort_should_returns_the_earliest_hits(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"sorting": {"field": "harvest.firstHarvested", "direction": "asc"}}
        result = client.post("/search", json=body)
        last_date = None
        for hit in result.json["hits"]:
            assert "harvest" in hit
            current_date = datetime.strptime(
                hit["harvest"]["firstHarvested"].split("T")[0], "%Y-%m-%d"
            )
            if last_date is not None:
                assert current_date >= last_date
            last_date = current_date

    @pytest.mark.integration
    def test_trailing_white_space_should_not_affect_result(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body_no_white_space = {"q": "landbruk"}
        body_white_space = {"q": "landbruk  "}

        no_white_space_result = client.post("/search", json=body_no_white_space).json
        white_space_result = client.post("/search", json=body_white_space).json
        assert json.dumps(no_white_space_result["page"]) == json.dumps(
            no_white_space_result["page"]
        )
        assert json.dumps(no_white_space_result["aggregations"]) == json.dumps(
            white_space_result["aggregations"]
        )
        assert json.dumps(no_white_space_result["hits"][0]) == json.dumps(
            white_space_result["hits"][0]
        )

    @pytest.mark.integration
    def test_words_in_title_after_exact_match(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"q": "barnehage", "size": 300}
        result = client.post("/search", json=body)
        last_was_word_in_title = False
        last_was_not_word_in_title = False
        last_title: Dict = {}
        for hit in result.json["hits"]:
            is_exact = is_exact_match_in_title(hit, "barnehage")
            if is_exact:
                assert last_was_word_in_title is False, (
                    "{0}: word in title encountered before exact "
                    "matches in title".format(get_title_values(hit))
                )
                assert last_was_not_word_in_title is False, (
                    "{0}: word not in title encountered before exact "
                    "matches in title".format(get_title_values(hit))
                )
            elif has_word_in_title(hit, "barnehage", ["barne", "hage"]):
                assert last_was_not_word_in_title is False, (
                    "{0}: word not in title encountered before word in title."
                    "Last title was: {1}".format(get_title_values(hit), last_title)
                )
                last_was_word_in_title = True
            else:
                last_was_not_word_in_title = True
                last_was_word_in_title = False
            last_title = get_title_values(hit)

    @pytest.mark.integration
    def test_filter_on_los_should_have_informationmodels_and_datasets(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"los": "helse-og-omsorg"}], "size": 100}
        result = client.post("/search", json=body)
        has_info_models = False
        has_datasets = False
        for hit in result.json["hits"]:
            if hit["type"] == "informationmodel":
                has_info_models = True
            elif hit["type"] == "dataset":
                has_datasets = True
            if has_info_models and has_datasets:
                break

        assert has_datasets is True
        assert has_info_models is True

    @pytest.mark.integration
    def test_filter_on_los_should_handle_filters_on_different_themes(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {
            "filters": [
                {"los": "helse-og-omsorg,naring"},
            ],
        }
        result = client.post("/search", json=body)
        assert len(result.json["hits"]) > 0

    @pytest.mark.integration
    def test_filter_on_los_should_handle_filters_om_sub_themes(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {
            "filters": [
                {"los": "helse-og-omsorg,helse-og-omsorg/svangerskap"},
            ],
        }
        result = client.post("/search", json=body).json
        assert len(result["hits"]) > 0

    @pytest.mark.integration
    def test_filter_on_los_themes_should_not_change_subtheme_content(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        empty_search = client.post("/search").json
        expected_themes = []
        for path in empty_search["aggregations"]["los"]["buckets"]:
            if len(re.findall("trafikk-og-transport", path["key"])) > 0:
                expected_themes.append(path)

        body = {
            "filters": [
                {"los": "trafikk-og-transport"},
            ],
        }
        result = client.post("/search", json=body).json
        result_themes = []
        for path in result["aggregations"]["los"]["buckets"]:
            if len(re.findall("trafikk-og-transport", path["key"])) > 0:
                result_themes.append(path)

        assert json.dumps(expected_themes) == json.dumps(result_themes)

    @pytest.mark.integration
    def test_result_should_have_theme_aggregations(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        result = client.post("/search")
        assert "theme" in result.json["aggregations"]

    @pytest.mark.integration
    def test_filter_on_eu_theme(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"theme": "GOVE"}], "size": 100}
        result = client.post("/search", json=body).json
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert "theme" in hit.keys()
            id_path = parse("theme[*].code")
            assert "GOVE" in [match.value for match in id_path.find(hit)]

    @pytest.mark.integration
    def test_filter_on_eu_theme_should_handle_filters_on_multiple_themes(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"theme": "GOVE,ENVI"}], "size": 100}

        result = client.post("/search", json=body).json
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert "theme" in hit.keys()
            id_path = parse("theme[*].code")
            assert "GOVE" in [match.value for match in id_path.find(hit)]
            assert "ENVI" in [match.value for match in id_path.find(hit)]

    @pytest.mark.integration
    def test_filter_on_eu_theme_ukjent(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"theme": "Ukjent"}], "size": 100}
        result = client.post("/search", json=body).json
        assert len(result["hits"]) > 0
        for hit in result["hits"]:
            assert hit["type"] == "dataset"
            for key in hit.keys():
                if key == "theme" and hit[key]:
                    for entry in hit[key]:
                        assert not entry.get("code")

    @pytest.mark.integration
    def test_filter_on_open_access(
        self, client: Flask, docker_service, api, wait_for_ready
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
    def test_filter_on_unknown_access_datasets(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"filters": [{"accessRights": "Ukjent"}]}
        result = client.post("/search", json=body).json
        assert len(result["hits"]) > 0
        assert (
            result["page"]["totalElements"]
            == result["aggregations"]["accessRights"]["buckets"][0]["doc_count"]
        )
        for hits in result["hits"]:
            assert not hits.get("accessRights")

    @pytest.mark.integration
    def test_search_with_empty_result_should_return_empty_object(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"q": "Ainjgulu"}

        result = client.post("/search", json=body).json
        assert len(result["hits"]) == 0

    @pytest.mark.integration
    def test_exits_filter(self, client: Flask, docker_service, api, wait_for_ready):
        body = {"filters": [{"exists": "subject,provenance.code"}], "size": 200}
        result = client.post("/search", json=body)
        assert result.status_code == 200
        hits = result.json["hits"]
        assert len(hits) > 0
        for hit in hits:
            keys = hit.keys()
            assert "subject" in keys
            assert "provenance" in keys
            assert "code" in hit["provenance"].keys()

    @pytest.mark.integration
    def test_special_chars_should_not_affect_result_length(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {"q": "Regnskapsregisteret jm"}
        body_special_char = {"q": "Regnskapsregisteret - jm"}
        expected = client.post("/search", json=body).json["page"]["totalElements"]
        result = client.post("/search", json=body_special_char).json
        assert result["page"]["totalElements"] == expected

    @pytest.mark.integration
    def test_collection_filter(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        body = {
            "filters": [
                {
                    "collection": {
                        "field": "uri",
                        "values": [
                            "https://registrering.staging.fellesdatakatalog.digdir.no/catalogs/910244132/datasets/e89629a3-701f-40f4-acae-fe422029da9f",
                            "https://registrering.staging.fellesdatakatalog.digdir.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2",
                        ],
                    }
                }
            ]
        }

        result = client.post("/search", json=body)
        assert result.status_code == 200
        assert len(result.json["hits"]) == 2
        uris = [x["uri"] for x in result.json["hits"]]
        assert (
            "https://registrering.staging.fellesdatakatalog.digdir.no/catalogs/910244132/datasets/e89629a3-701f-40f4-acae-fe422029da9f"
            in uris
        )
        assert (
            "https://registrering.staging.fellesdatakatalog.digdir.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2"
            in uris
        )

    @pytest.mark.integration
    def test_search_all_total_should_be_sum_of_indices(
        self, client: Flask, docker_service, api, wait_for_ready
    ):
        total_all = client.post("/search").json["page"]["totalElements"]
        total_datasets = client.post("/datasets").json["page"]["totalElements"]
        total_services = client.post("/dataservices").json["page"]["totalElements"]
        total_concepts = client.post("/concepts").json["page"]["totalElements"]
        total_models = client.post("/informationmodels").json["page"]["totalElements"]

        assert total_all == sum(
            [total_datasets, total_services, total_concepts, total_models]
        )


def is_exact_match(keys, hit, search):
    for key in keys:
        if hit[key].lower() == search:
            return True
    return False


def is_exact_match_in_title(hit, srch_string):
    if "prefLabel" in hit:
        pref_labels = hit["prefLabel"]
        if is_exact_match(pref_labels.keys(), pref_labels, srch_string):
            return True
    elif "title" in hit:
        title = hit["title"]
        if isinstance(title, dict):
            if is_exact_match(title.keys(), title, srch_string):
                return True
        else:
            if title.lower() == srch_string:
                return True
    return False


def has_word_in_title(hit, search_string, search_string_parts=None):
    if search_string_parts is None:
        search_string_parts = []
    if "prefLabel" in hit:
        pref_labels = hit["prefLabel"]
        prt1 = re.findall(search_string.lower(), json.dumps(pref_labels).lower())
        prt2 = 0
        if search_string_parts:
            for part in search_string_parts:
                partial_matches = re.findall(part, json.dumps(pref_labels))
                prt2 += partial_matches.__len__()
        if len(prt1) > 0 or prt2 > 0:
            return True
    elif "title" in hit:
        title = hit["title"]
        prt1 = re.findall(search_string.lower(), json.dumps(title).lower())
        if len(prt1) > 0:
            return True
    return False


def get_title_values(hit):
    """get values of all title fields for hit"""
    if "prefLabel" in hit:
        return json.dumps(hit["prefLabel"])
    elif "title" in hit:
        return json.dumps(hit["title"])


def is_match_in_descriptive_texts(match_str: str, hit: dict) -> bool:
    description_text = get_descriptive_texts(hit)
    if description_text is None:
        return False
    else:
        return (
            len(
                re.findall(get_matches_with_stemming_regex(match_str), description_text)
            )
            > 0
        )


def get_descriptive_texts(hit: dict) -> Optional[str]:
    data_type = hit.get("type")
    try:
        if data_type == "concept":
            return json.dumps(hit.get("definition").get("text"))  # type: ignore
        elif data_type == "dataset":
            return json.dumps(hit.get("description").get("text"))  # type: ignore
        elif data_type == "dataservice":
            return json.dumps(hit.get("description"))
        elif data_type == "informationmodel":
            return str(hit.get("schema"))
        else:
            return None
    except AttributeError:
        return None


def get_matches_with_stemming_regex(match_str: str):
    all_matches: List = []
    all_matches.extend(
        m.lower() for m in match_str.split("en") if len(m) > 1 and m != ""
    )
    all_matches.extend(
        m.lower() for m in match_str.split("ens") if len(m) > 1 and m != ""
    )
    all_matches.extend(
        m.lower() for m in match_str.split("er") if len(m) > 1 and m != ""
    )
    all_matches.extend(
        m.lower() for m in match_str.split(" ") if len(m) > 1 and m != ""
    )
    return "|".join(m.lower() for m in all_matches)


def get_time(timestamp: str):
    return datetime.strptime(timestamp.split("T")[0], "%Y-%M-%d")
