import abc
from enum import Enum

from src.search.fields import index_suggestion_fields, index_title_fields
from src.search.query_utils import *
from src.search.themeprofiles import theme_profile_filter


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"

class AbstractSearchQuery(metaclass=abc.ABCMeta):

    def __init__(self, search_string: str = None):
        self.body = query_template()
        if search_string:
            self.query = dismax_template()

    def add_page(self, size: int = 10, page: int = None) -> dict:
        if size is None:
            size = 10
        self.body['size'] = size
        if page is not None:
            self.body['from'] = page * size

    def add_filters(self, filters: list):
        self.body["query"]["bool"]["filter"] = []
        for f in filters:
            key = list(f.keys())[0]
            if key == 'themeprofile':
                self.body["query"]["bool"]["filter"].append(theme_profile_filter(f[key]))
            elif (f[key]) == 'MISSING' or (f[key]) == 'Ukjent':
                self.body["query"]["bool"]["filter"].append(must_not_filter(key))
            elif f.get("collection", {}).get("values") and f.get("collection", {}).get("values")[0] == 'MISSING':
                self.body["query"]["bool"]["filter"].append(must_not_filter(f.get(key).get("field")))
            elif key == 'opendata':
                self.body["query"]["bool"]["filter"].append(open_data_query())
            elif key == 'exists':
                self.body["query"]["bool"]["filter"].extend(get_exists_filter(f))
            elif key == 'last_x_days':
                x_days_query = get_last_x_days_filter(f)
                self.body["query"]["bool"]["filter"].append(x_days_query)
            elif key == 'collection':
                self.body["query"]["bool"]["filter"].append(collection_filter(f[key]))
            elif key == 'catalog_name':
                catalog_name_query = get_catalogs_by_name(f['catalog_name'])
                self.body["query"]["bool"]["filter"].append(catalog_name_query)
            elif key == 'keywords':
                self.body["query"]["bool"]["filter"].append(keyword_filter(f[key]))
            elif key == 'info_model':
                self.body["query"]["bool"]["filter"].append(info_model_filter(f[key]))
            elif key == 'required_by_service':
                self.body["query"]["bool"]["filter"].append(required_by_service_filter(f[key]))
            elif key == 'related_by_service':
                self.body["query"]["bool"]["filter"].append(related_by_service_filter(f[key]))
            elif key == 'event':
                self.body["query"]["bool"]["filter"].append(event_filter(f[key]))
            else:
                self.body["query"]["bool"]["filter"].extend(get_term_filter(f))

    def add_sorting(self, param: dict):
        self.body["sort"] = {
            param.get("field"): {
                "order": param.get("direction"),
                "unmapped_type": "long"
            }
        }

    @abc.abstractmethod
    def add_aggs(self, fields: list):
        pass

    @abc.abstractmethod
    def add_search_string(self, search_string: str):
        pass


class AllIndicesQuery(AbstractSearchQuery):

    def __init__(self, search_string=None, aggs=None, filters=None):
        super().__init__(search_string)
        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.body["indices_boost"] = [{"datasets": 1.2}]
            self.query = all_indices_default_query()
        if aggs is None:
            self.add_aggs()
        if filters:
            self.body["query"] = query_with_filter_template(must_clause=[self.query])
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_aggs(self, fields=None):
        # TODO user defined aggs
        if fields is None:
            self.body["aggs"] = default_all_indices_aggs()

    def add_search_string(self, param: str):
        self.query["dis_max"]["queries"].append(exact_match_in_title_query(
            title_field_names=["prefLabel.*", "title.*", "title"],
            search_string=param))
        self.query["dis_max"]["queries"].append(
            word_in_title_query(title_field_names=["title.*", "title", "prefLabel.*"],
                                search_string=param))
        self.query["dis_max"]["queries"].append(match_on_publisher_name_query(param))
        self.query["dis_max"]["queries"].append(
            word_in_description_query(
                index_key=IndicesKey.ALL,
                search_string=param))
        some_words_in_title = some_words_in_title_query(title_fields_list=["title.*", "title", "prefLabel.*"],
                                                        search_string=param)
        if some_words_in_title:
            self.query["dis_max"]["queries"].append(some_words_in_title)

        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param,
                                                                    boost=0.0015,
                                                                    all_indices_autorativ_boost=True))
        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param,
                                                                    boost=0.001,
                                                                    lenient=True,
                                                                    all_indices_autorativ_boost=True
                                                                    ))


class InformationModelQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)
        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = {"match_all": {}}

        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_filter_template(must_clause=[self.query])
                self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_search_string(self, search_string: str):
        dismax_queries = [index_match_in_title_query(index_key=IndicesKey.INFO_MODEL,
                                                     search_string=search_string),
                          word_in_description_query(index_key=IndicesKey.INFO_MODEL,
                                                    search_string=search_string,
                                                    autorativ_boost=False),
                          simple_query_string(search_string=search_string,
                                              all_indices_autorativ_boost=False,
                                              boost=0.02,
                                              fields_for_index=IndicesKey.INFO_MODEL),
                          simple_query_string(search_string=search_string,
                                              all_indices_autorativ_boost=False,
                                              lenient=True,
                                              fields_for_index=IndicesKey.INFO_MODEL)]
        self.query["dis_max"]["queries"] = dismax_queries

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["los"] = los_aggregation()
            self.body["aggs"]["orgPath"] = org_path_aggregation()
        # TODO implement user defined aggregations?


class DataServiceQuery(AbstractSearchQuery):
    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = {"match_all": {}}

        self.add_aggs(aggs)
        if filters:
            self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                 should_clause=[],
                                                                 filter_clause=True)
            self.add_filters(filters)
        else:
            self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                 should_clause=[])

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["orgPath"] = org_path_aggregation()
            self.body["aggs"]["formats"] = get_aggregation_term_for_key(aggregation_key="mediaType.code.keyword")

    def add_search_string(self, search_string: str):
        dismax_queries = [
            index_match_in_title_query(index_key=IndicesKey.DATA_SERVICES,
                                       search_string=search_string),
            word_in_description_query(index_key=IndicesKey.DATA_SERVICES,
                                      search_string=search_string,
                                      autorativ_boost=False),
            simple_query_string(search_string=search_string,
                                all_indices_autorativ_boost=False,
                                boost=0.02,
                                fields_for_index=IndicesKey.DATA_SERVICES),
            simple_query_string(search_string=search_string,
                                all_indices_autorativ_boost=False,
                                lenient=True,
                                fields_for_index=IndicesKey.DATA_SERVICES)
        ]
        self.query["dis_max"]["queries"] = dismax_queries


class DataSetQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = {"match_all": {}}
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                     should_clause=[autorativ_dataset_query(),
                                                                                    open_data_query()],
                                                                     filter_clause=True)
                self.add_filters(filters)
        else:
            self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                 should_clause=[autorativ_dataset_query(),
                                                                                open_data_query()])

    def add_search_string(self, search_string: str):
        dismax_queries = [
            index_match_in_title_query(index_key=IndicesKey.DATA_SETS, search_string=search_string, boost=5),
            word_in_description_query(index_key=IndicesKey.DATA_SETS,
                                      search_string=search_string,
                                      autorativ_boost=False),
            simple_query_string(search_string=search_string, boost=0.5, fields_for_index=IndicesKey.DATA_SETS),
            simple_query_string(search_string=search_string,
                                all_indices_autorativ_boost=False,
                                lenient=True,
                                fields_for_index=IndicesKey.DATA_SETS)
        ]
        self.query["dis_max"]["queries"] = dismax_queries

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["los"] = los_aggregation()
            self.body["aggs"]["provenance"] = get_aggregation_term_for_key(aggregation_key="provenance")
            self.body["aggs"]["orgPath"] = org_path_aggregation()
            self.body["aggs"]["opendata"] = {
                "filter": open_data_query()
            }
            self.body["aggs"]["theme"] = get_aggregation_term_for_key(aggregation_key="theme")
            self.body["aggs"]["accessRights"] = get_aggregation_term_for_key(aggregation_key="accessRights",
                                                                             missing="Ukjent",
                                                                             size=10)
            self.body["aggs"]["spatial"] = get_aggregation_term_for_key(aggregation_key="spatial")

class ConceptQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = {"match_all": {}}
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                    should_clause=[],
                                                                     filter_clause=True)
                self.add_filters(filters)
        else:
            self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                 should_clause=[])

    def add_search_string(self, search_string: str):
        dismax_queries = [
            exact_match_in_title_query(index_title_fields[IndicesKey.CONCEPTS], search_string=search_string),
            index_match_in_title_query(index_key=IndicesKey.CONCEPTS, search_string=search_string, boost=10),
            word_in_description_query(index_key=IndicesKey.CONCEPTS,
                                      search_string=search_string,
                                      autorativ_boost=False),
            simple_query_string(search_string=search_string,
                                        all_indices_autorativ_boost=False,
                                        boost=0.02,
                                        fields_for_index=IndicesKey.CONCEPTS),
            simple_query_string(search_string=search_string,
                                        all_indices_autorativ_boost=False,
                                        lenient=True,
                                        fields_for_index=IndicesKey.CONCEPTS)]
        self.query["dis_max"]["queries"] = dismax_queries

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["los"] = los_aggregation()
            self.body["aggs"]["provenance"] = get_aggregation_term_for_key(aggregation_key="provenance")
            self.body["aggs"]["orgPath"] = org_path_aggregation()
            self.body["aggs"]["opendata"] = {
                "filter": open_data_query()
            }
            self.body["aggs"]["theme"] = get_aggregation_term_for_key(aggregation_key="theme")
            self.body["aggs"]["accessRights"] = get_aggregation_term_for_key(aggregation_key="accessRights",
                                                                             missing="Ukjent",
                                                                             size=10)
            self.body["aggs"]["spatial"] = get_aggregation_term_for_key(aggregation_key="spatial")


class PublicServiceQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = {"match_all": {}}
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                    should_clause=[],
                                                                     filter_clause=True)
                self.add_filters(filters)
        else:
            self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                 should_clause=[])

    def add_search_string(self, search_string: str):
        dismax_queries = [
            exact_match_in_title_query(index_title_fields[IndicesKey.PUBLIC_SERVICES], search_string=search_string),
            index_match_in_title_query(index_key=IndicesKey.PUBLIC_SERVICES, search_string=search_string, boost=10),
            word_in_description_query(index_key=IndicesKey.PUBLIC_SERVICES,
                                      search_string=search_string,
                                      autorativ_boost=False),
            simple_query_string(search_string=search_string,
                                        all_indices_autorativ_boost=False,
                                        boost=0.02),
            simple_query_string(search_string=search_string,
                                        all_indices_autorativ_boost=False,
                                        lenient=True)]
        self.query["dis_max"]["queries"] = dismax_queries

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["hasCompetentAuthority"] = hasCompetentAuthority_aggregation()
            self.body["aggs"]["isGroupedBy"] = is_grouped_by_aggregation()


class EventQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = {"match_all": {}}
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                     should_clause=[],
                                                                     filter_clause=True)
                self.add_filters(filters)
        else:
            self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                 should_clause=[])

    def add_search_string(self, search_string: str):
        dismax_queries = [
            exact_match_in_title_query(index_title_fields[IndicesKey.EVENTS], search_string=search_string),
            index_match_in_title_query(index_key=IndicesKey.EVENTS, search_string=search_string, boost=10),
            word_in_description_query(index_key=IndicesKey.EVENTS,
                                      search_string=search_string,
                                      autorativ_boost=False),
            simple_query_string(search_string=search_string,
                                all_indices_autorativ_boost=False,
                                boost=0.02),
            simple_query_string(search_string=search_string,
                                all_indices_autorativ_boost=False,
                                lenient=True)]
        self.query["dis_max"]["queries"] = dismax_queries

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["hasCompetentAuthority"] = hasCompetentAuthority_aggregation()


class PublicServicesAndEventsQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)

        if search_string:
            self.add_search_string(search_string)
        else:
            self.body["indices_boost"] = [{"public_services": 1.2}]
            self.query = {"match_all": {}}
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                     should_clause=[],
                                                                     filter_clause=True)
                self.add_filters(filters)
        else:
            self.body["query"] = query_with_final_boost_template(must_clause=[self.query],
                                                                 should_clause=[])

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["hasCompetentAuthority"] = hasCompetentAuthority_aggregation()
            self.body["aggs"]["isGroupedBy"] = is_grouped_by_aggregation()
            self.body["aggs"]["associatedBroaderTypesByEvents"] = associated_broader_types_by_events_aggregation()

    def add_search_string(self, param: str):
        self.query["dis_max"]["queries"].append(exact_match_in_title_query(
            title_field_names=["prefLabel.*", "title.*", "title"],
            search_string=param))
        self.query["dis_max"]["queries"].append(
            word_in_title_query(title_field_names=["title.*", "title", "prefLabel.*"],
                                search_string=param))
        self.query["dis_max"]["queries"].append(match_on_publisher_name_query(param))
        self.query["dis_max"]["queries"].append(
            word_in_description_query(
                index_key=IndicesKey.ALL,
                search_string=param))
        some_words_in_title = some_words_in_title_query(title_fields_list=["title.*", "title", "prefLabel.*"],
                                                        search_string=param)
        if some_words_in_title:
            self.query["dis_max"]["queries"].append(some_words_in_title)

        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param,
                                                                    boost=0.0015,
                                                                    all_indices_autorativ_boost=True))
        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param,
                                                                    boost=0.001,
                                                                    lenient=True,
                                                                    all_indices_autorativ_boost=True
                                                                    ))


class RecentQuery:
    def __init__(self, size=None):
        self.query = {
            "size": 5,
            "sort": {"harvest.firstHarvested": {
                "order": Direction.DESC.value,
                "unmapped_type": "long"
            }
            }
        }

        if size is not None:
            self.query["size"] = size


class SuggestionQuery:
    def __init__(self, index_key, search_string):
        self.body = {
            "_source": index_suggestion_fields[index_key],
            "query": suggestion_title_query(index_key=index_key, search_string=search_string)
        }
