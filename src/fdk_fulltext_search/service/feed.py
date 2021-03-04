from enum import Enum
import os
from typing import Any, Dict, Iterable
from urllib.parse import urlencode

from feedgen.feed import FeedGenerator
from flask import request

from fdk_fulltext_search.ingest import IndicesKey
from fdk_fulltext_search.search import client


FDK_BASE_URI = os.getenv("FDK_BASE_URI", "https://staging.fellesdatakatalog.digdir.no")


class FeedType(Enum):
    RSS = "rss"
    ATOM = "atom"


def create_feed(feed_type: FeedType) -> str:
    feed_generator = FeedGenerator()

    search_params = extract_search_params(request.args)

    base_url = f"{FDK_BASE_URI}/datasets"
    query_string = build_query_string(search_params)

    feed_generator.id(f"{base_url}{query_string}")
    feed_generator.title("Felles datakatalog - Datasett")
    feed_generator.description("En samling av datasett publisert i Felles datakataog")
    feed_generator.link(href=f"{base_url}{query_string}")

    datasets = get_datasets_for_feed(
        map_search_params_to_search_request_body(search_params)
    )

    for dataset in datasets:
        feed_entry = feed_generator.add_entry()

        feed_entry.id(f"{base_url}/{dataset['id']}")
        feed_entry.title(translate(dataset["title"]))
        feed_entry.description(translate(dataset["description"]))
        feed_entry.link(href=f"{base_url}/{dataset['id']}")
        feed_entry.author(
            name=translate(
                dataset["publisher"]["prefLabel"] or dataset["publisher"]["name"]
            )
        )
        feed_entry.published(dataset["harvest"]["firstHarvested"])

    if feed_type == FeedType.RSS:
        return feed_generator.rss_str(pretty=True)
    elif feed_type == FeedType.ATOM:
        return feed_generator.atom_str(pretty=True)
    else:
        return ""


def get_datasets_for_feed(search_request_body: Dict[str, Any]) -> Iterable[Dict]:
    results = client.search_in_index(
        index=IndicesKey.DATA_SETS,
        request={
            "q": search_request_body["q"],
            "filters": [*search_request_body["filters"], {"last_x_days": 1}],
            "sorting": {"field": "harvest.firstHarvested", "direction": "desc"},
            "size": 1000,
        },
    )

    if results["hits"] and results["hits"]["hits"]:
        return map(lambda hit: hit["_source"], results["hits"]["hits"])

    return []


def translate(translatable: Dict[str, str]) -> str:
    return (
        translatable["nb"]
        or translatable["no"]
        or translatable["nn"]
        or translatable["en"]
    )


def extract_search_params(params: Dict[str, str]) -> Dict[str, str]:
    search_params = {
        "q": params.get("q"),
        "losTheme": params.get("losTheme"),
        "theme": params.get("theme"),
        "opendata": params.get("opendata"),
        "accessrights": params.get("accessrights"),
        "orgPath": params.get("orgPath"),
        "spatial": params.get("spatial"),
        "provenance": params.get("provenance"),
        "sortfield": "harvest.firstHarvested",
    }

    return {k: v for k, v in search_params.items() if v is not None}


def map_search_params_to_search_request_body(params: Dict[str, str]) -> Dict[str, Any]:
    filters = []

    if "losTheme" in params:
        filters.append({"los": params["losTheme"]})

    if "theme" in params:
        filters.append({"theme": params["theme"]})

    if "opendata" in params:
        filters.append({"opendata": True})

    if "accessrights" in params:
        filters.append({"accessRights": params["accessrights"]})

    if "orgPath" in params:
        filters.append({"orgPath": params["orgPath"]})

    if "spatial" in params:
        filters.append({"spatial": params["spatial"]})

    if "provenance" in params:
        filters.append({"provenance": params["provenance"]})

    return {"q": params["q"] if "q" in params else "", "filters": filters}


def build_query_string(params: Dict[str, str]) -> str:
    return f"?{urlencode(params)}" if len(params) > 0 else ""
