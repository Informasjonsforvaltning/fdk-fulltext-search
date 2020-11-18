from enum import Enum
from typing import Iterable, Dict
from feedgen.feed import FeedGenerator
from flask import request

from src.search import client
from src.ingest import IndicesKey


class FeedType(Enum):
    RSS = "rss"
    ATOM = "atom"


def create_feed(feed_type: FeedType) -> str:
    feed_generator = FeedGenerator()

    feed_generator.id(request.url)
    feed_generator.title("Felles datakatalog - Datasett")
    feed_generator.description("En samling av datasett publisert i Felles datakataog")
    feed_generator.link(href=request.url)

    datasets = get_datasets_for_feed()

    for dataset in datasets:
        feed_entry = feed_generator.add_entry()

        feed_entry.id(f"{request.url}/{dataset['id']}")
        feed_entry.title(translate(dataset["title"]))
        feed_entry.description(translate(dataset["description"]))
        feed_entry.link(href=f"{request.url}/{dataset['id']}")
        feed_entry.author(name=translate(dataset["publisher"]["prefLabel"] or dataset["publisher"]["name"]))
        feed_entry.published(dataset["harvest"]["firstHarvested"])

    if feed_type == FeedType.RSS:
        return feed_generator.rss_str(pretty=True)
    elif feed_type == FeedType.ATOM:
        return feed_generator.atom_str(pretty=True)
    else:
        return ""


def get_datasets_for_feed() -> Iterable[Dict]:
    results = client.search_in_index(
        index=IndicesKey.DATA_SETS,
        request={
            "filters": [
                {
                    "last_x_days": 1
                }
            ],
            "sorting": {
                "field": "harvest.firstHarvested",
                "direction": "desc"
            },
            "size": 1000
        }
    )

    if results["hits"] and results["hits"]["hits"]:
        return map(lambda hit: hit["_source"], results["hits"]["hits"])

    return []


def translate(translatable: Dict[str, str]) -> str:
    return translatable["nb"] or translatable["no"] or translatable["nn"] or translatable["en"]
