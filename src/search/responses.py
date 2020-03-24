from dataclasses import dataclass


@dataclass
class Page:
    size: int
    totalElements: int
    currentPage: int

@dataclass
class Aggregations:
    name: str

@dataclass
class SearchResponse:
    hits: dict
    page: Page
    aggregations: Aggregations
