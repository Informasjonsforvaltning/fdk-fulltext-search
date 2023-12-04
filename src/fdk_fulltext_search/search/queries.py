import abc
from enum import Enum
from typing import Any, Dict, List, Optional

from fdk_fulltext_search.ingest.utils import IndicesKey
from fdk_fulltext_search.search.field_utils import (
    description_fields,
    fulltext_fields,
    suggestion_fields,
    title_fields,
)
import fdk_fulltext_search.search.query_aggregation_utils as query_aggregation_utils
import fdk_fulltext_search.search.query_filter_utils as query_filter_utils
import fdk_fulltext_search.search.query_utils as query_utils
from fdk_fulltext_search.search.themeprofiles import theme_profile_filter


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"


class AbstractSearchQuery(metaclass=abc.ABCMeta):
    def __init__(self: Any, search_string: Optional[str] = None) -> None:
        self.body = query_utils.query_template()
        if search_string:
            self.query = query_utils.dismax_template()

    def add_page(
        self: Any, size: Optional[int] = None, page: Optional[int] = None
    ) -> None:
        if size is None:
            size = 10
        self.body["size"] = size
        if page is not None:
            self.body["from"] = page * size

    def add_filters(self: Any, filters: List) -> None:
        self.body["query"]["bool"]["filter"] = []
        for f in filters:
            key = list(f.keys())[0]
            if key == "themeprofile":
                self.body["query"]["bool"]["filter"].append(
                    theme_profile_filter(f[key])
                )
            elif (f[key]) == "MISSING" or (f[key]) == "Ukjent":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.must_not_filter(key)
                )
            elif (
                f.get("collection", {}).get("values")
                and f.get("collection", {}).get("values")[0] == "MISSING"
            ):
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.must_not_filter(f.get(key).get("field"))
                )
            elif key == "opendata":
                if f[key] == "false":
                    self.body["query"]["bool"]["filter"].append(
                        query_utils.must_not_be_open_data_query()
                    )
                else:
                    self.body["query"]["bool"]["filter"].append(
                        query_utils.open_data_query()
                    )
            elif key == "exists":
                self.body["query"]["bool"]["filter"].extend(
                    query_filter_utils.exists_filter(f)
                )
            elif key == "last_x_days":
                x_days_query = query_filter_utils.last_x_days_filter(f)
                self.body["query"]["bool"]["filter"].append(x_days_query)
            elif key == "collection":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.collection_filter(f[key])
                )
            elif key == "catalog_name":
                catalog_name_query = query_filter_utils.catalogs_by_name_filter(f[key])
                self.body["query"]["bool"]["filter"].append(catalog_name_query)
            elif key == "keywords":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.keyword_filter(f[key])
                )
            elif key == "info_model":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.info_model_filter(f[key])
                )
            elif key == "required_by_service":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.required_by_service_filter(f[key])
                )
            elif key == "related_by_service":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.related_by_service_filter(f[key])
                )
            elif key == "event":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.event_filter(f[key])
                )
            elif key == "eventType":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.event_type_filter(f[key])
                )
            elif key == "informationmodel_relation":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.information_model_by_relation_filter(f[key])
                )
            elif key == "requires_or_relates":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.requires_or_relates_filter(f[key])
                )
            elif key == "dataset_info_model_relations":
                self.body["query"]["bool"]["filter"].append(
                    query_filter_utils.dataset_info_model_relations_filter(f[key])
                )
            else:
                self.body["query"]["bool"]["filter"].extend(
                    query_filter_utils.term_filter(f)
                )

    def add_sorting(self: Any, param: Dict) -> None:
        self.body["sort"] = {
            param.get("field"): {
                "order": param.get("direction"),
                "unmapped_type": "long",
            }
        }

    @abc.abstractmethod
    def add_aggs(self: Any, fields: List) -> Any:
        pass

    @abc.abstractmethod
    def add_search_string(self: Any, search_string: str) -> Any:
        pass


class AllIndicesQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)
        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.body["indices_boost"] = [{"datasets": 1.2}]
            self.query = query_utils.default_query()
        if aggs is None:
            self.add_aggs()
        if filters:
            self.body["query"] = query_utils.query_with_filter_template(
                must_clause=[self.query]
            )
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_aggs(self: Any, fields: Optional[List] = None) -> Any:
        # TODO user defined aggs
        if fields is None:
            self.body["aggs"] = query_aggregation_utils.default_all_indices_aggs()

    def add_search_string(self: Any, param: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields(
                    [
                        IndicesKey.CONCEPTS,
                        IndicesKey.DATA_SERVICES,
                        IndicesKey.DATA_SETS,
                        IndicesKey.EVENTS,
                        IndicesKey.INFO_MODEL,
                        IndicesKey.PUBLIC_SERVICES,
                    ]
                ),
                search_string=param,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields(
                    [
                        IndicesKey.CONCEPTS,
                        IndicesKey.DATA_SERVICES,
                        IndicesKey.DATA_SETS,
                        IndicesKey.EVENTS,
                        IndicesKey.INFO_MODEL,
                        IndicesKey.PUBLIC_SERVICES,
                    ]
                ),
                search_string=param,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(param)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields(
                    [
                        IndicesKey.CONCEPTS,
                        IndicesKey.DATA_SERVICES,
                        IndicesKey.DATA_SETS,
                        IndicesKey.EVENTS,
                        IndicesKey.INFO_MODEL,
                        IndicesKey.PUBLIC_SERVICES,
                    ]
                ),
                search_string=param,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields(
                    [
                        IndicesKey.CONCEPTS,
                        IndicesKey.DATA_SERVICES,
                        IndicesKey.DATA_SETS,
                        IndicesKey.EVENTS,
                        IndicesKey.INFO_MODEL,
                        IndicesKey.PUBLIC_SERVICES,
                    ]
                ),
                search_string=param,
            )
        )


class InformationModelQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)
        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.query = query_utils.default_query()

        self.add_aggs(aggs)
        if filters:
            self.body["query"] = query_utils.query_with_filter_template(
                must_clause=[self.query]
            )
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_search_string(self: Any, search_string: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields([IndicesKey.INFO_MODEL]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields([IndicesKey.INFO_MODEL]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(search_string)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields([IndicesKey.INFO_MODEL]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields([IndicesKey.INFO_MODEL]),
                search_string=search_string,
            )
        )

    def add_aggs(self: Any, fields: List) -> Any:
        if fields is None:
            self.body["aggs"]["los"] = query_aggregation_utils.los_aggregation()
            self.body["aggs"][
                "orgPath"
            ] = query_aggregation_utils.org_path_aggregation()
        # TODO implement user defined aggregations?


class DataServiceQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.query = query_utils.default_query()

        self.add_aggs(aggs)
        if filters:
            self.body["query"] = query_utils.query_with_filter_template(
                must_clause=[self.query]
            )
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_aggs(self: Any, fields: List) -> Any:
        if fields is None:
            self.body["aggs"][
                "orgPath"
            ] = query_aggregation_utils.org_path_aggregation()
            self.body["aggs"][
                "format"
            ] = query_aggregation_utils.fdk_format_aggregation()

    def add_search_string(self: Any, search_string: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields([IndicesKey.DATA_SERVICES]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields([IndicesKey.DATA_SERVICES]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(search_string)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields([IndicesKey.DATA_SERVICES]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields([IndicesKey.DATA_SERVICES]),
                search_string=search_string,
            )
        )


class DataSetQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.query = query_utils.default_query()
        self.add_aggs(aggs)
        if filters:
            self.body["query"] = query_utils.query_with_filter_template(
                must_clause=[self.query]
            )
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_search_string(self: Any, search_string: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields([IndicesKey.DATA_SETS]), search_string=search_string
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields([IndicesKey.DATA_SETS]), search_string=search_string
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(search_string)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields([IndicesKey.DATA_SETS]),
                search_string=search_string,
            ),
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields([IndicesKey.DATA_SETS]),
                search_string=search_string,
            )
        )

    def add_aggs(self: Any, fields: List) -> Any:
        if fields is None:
            self.body["aggs"][
                "format"
            ] = query_aggregation_utils.fdk_format_aggregation()
            self.body["aggs"]["los"] = query_aggregation_utils.los_aggregation()
            self.body["aggs"][
                "provenance"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="provenance"
            )
            self.body["aggs"][
                "orgPath"
            ] = query_aggregation_utils.org_path_aggregation()
            self.body["aggs"]["opendata"] = {"filter": query_utils.open_data_query()}
            self.body["aggs"][
                "theme"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="theme"
            )
            self.body["aggs"][
                "accessRights"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="accessRights", missing="Ukjent", size=10
            )
            self.body["aggs"][
                "spatial"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="spatial"
            )


class ConceptQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.query = query_utils.default_query()
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_utils.query_with_filter_template(
                    must_clause=[self.query]
                )
                self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_search_string(self: Any, search_string: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields([IndicesKey.CONCEPTS]), search_string=search_string
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields([IndicesKey.CONCEPTS]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(search_string)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields([IndicesKey.CONCEPTS]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields([IndicesKey.CONCEPTS]),
                search_string=search_string,
            )
        )

    def add_aggs(self: Any, fields: list) -> Any:
        if fields is None:
            self.body["aggs"]["los"] = query_aggregation_utils.los_aggregation()
            self.body["aggs"][
                "provenance"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="provenance"
            )
            self.body["aggs"][
                "orgPath"
            ] = query_aggregation_utils.org_path_aggregation()
            self.body["aggs"]["opendata"] = {"filter": query_utils.open_data_query()}
            self.body["aggs"][
                "theme"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="theme"
            )
            self.body["aggs"][
                "accessRights"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="accessRights", missing="Ukjent", size=10
            )
            self.body["aggs"][
                "spatial"
            ] = query_aggregation_utils.get_aggregation_term_for_key(
                aggregation_key="spatial"
            )


class PublicServiceQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.query = query_utils.default_query()
        self.add_aggs(aggs)
        if filters:
            self.body["query"] = query_utils.query_with_filter_template(
                must_clause=[self.query]
            )
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_search_string(self: Any, search_string: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields([IndicesKey.PUBLIC_SERVICES]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields([IndicesKey.PUBLIC_SERVICES]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(search_string)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields([IndicesKey.PUBLIC_SERVICES]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields([IndicesKey.PUBLIC_SERVICES]),
                search_string=search_string,
            )
        )

    def add_aggs(self: Any, fields: List) -> Any:
        if fields is None:
            self.body["aggs"][
                "hasCompetentAuthority"
            ] = query_aggregation_utils.has_competent_authority_aggregation()
            self.body["aggs"][
                "ownedBy"
            ] = query_aggregation_utils.owned_by_aggregation()
            self.body["aggs"][
                "isGroupedBy"
            ] = query_aggregation_utils.is_grouped_by_aggregation()


class EventQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.query = query_utils.default_query()
        self.add_aggs(aggs)
        if filters:
            self.body["query"] = query_utils.query_with_filter_template(
                must_clause=[self.query]
            )
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_search_string(self: Any, search_string: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields([IndicesKey.EVENTS]), search_string=search_string
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields([IndicesKey.EVENTS]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(search_string)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields([IndicesKey.EVENTS]),
                search_string=search_string,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields([IndicesKey.EVENTS]), search_string=search_string
            )
        )

    def add_aggs(self: Any, fields: List) -> Any:
        if fields is None:
            self.body["aggs"][
                "hasCompetentAuthority"
            ] = query_aggregation_utils.has_competent_authority_aggregation()


class PublicServicesAndEventsQuery(AbstractSearchQuery):
    def __init__(
        self: Any,
        search_string: Optional[str] = None,
        aggs: Optional[List] = None,
        filters: Optional[List] = None,
    ) -> None:
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.body["indices_boost"] = [{"public_services": 1.2}]
            self.query = query_utils.default_query()
        self.add_aggs(aggs)
        if filters:
            self.body["query"] = query_utils.query_with_filter_template(
                must_clause=[self.query]
            )
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_aggs(self: Any, fields: List) -> Any:
        if fields is None:
            self.body["aggs"][
                "hasCompetentAuthority"
            ] = query_aggregation_utils.has_competent_authority_aggregation()
            self.body["aggs"][
                "ownedBy"
            ] = query_aggregation_utils.owned_by_aggregation()
            self.body["aggs"][
                "isGroupedBy"
            ] = query_aggregation_utils.is_grouped_by_aggregation()
            self.body["aggs"][
                "associatedBroaderTypesByEvents"
            ] = query_aggregation_utils.associated_broader_types_by_events_aggregation()

    def add_search_string(self: Any, param: str) -> Any:
        self.query["dis_max"]["queries"].append(
            query_utils.title_exact_match_query(
                fields=title_fields([IndicesKey.EVENTS, IndicesKey.PUBLIC_SERVICES]),
                search_string=param,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.title_query(
                fields=title_fields([IndicesKey.EVENTS, IndicesKey.PUBLIC_SERVICES]),
                search_string=param,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.organization_and_keyword_query(param)
        )
        self.query["dis_max"]["queries"].append(
            query_utils.description_query(
                fields=description_fields(
                    [IndicesKey.EVENTS, IndicesKey.PUBLIC_SERVICES]
                ),
                search_string=param,
            )
        )
        self.query["dis_max"]["queries"].append(
            query_utils.simple_query_string(
                fields=fulltext_fields([IndicesKey.EVENTS, IndicesKey.PUBLIC_SERVICES]),
                search_string=param,
            )
        )


class RecentQuery:
    def __init__(self: Any, size: Optional[int] = None) -> None:
        self.query = {
            "size": 5,
            "sort": {
                "harvest.firstHarvested": {
                    "order": Direction.DESC.value,
                    "unmapped_type": "long",
                }
            },
        }

        if size is not None:
            self.query["size"] = size


class SuggestionQuery:
    def __init__(
        self: Any,
        indices: List[str],
        search_string: str,
        is_transport: bool,
        publisher_id: Optional[str] = None,
    ) -> None:
        self.body = {
            "_source": suggestion_fields(indices),
            "query": query_utils.title_suggestion_query(
                fields=title_fields(indices),
                search_string=search_string,
                is_transport=is_transport,
                publisher_id=publisher_id,
            ),
        }
