import json
import os

from flask_restful import Resource, abort
from flask import request, Response

from .search import client
from .ingest import fetch_all_content, IndicesKey, fetch_data_sets, fetch_information_models, \
    fetch_data_services, fetch_concepts, fetch_public_services, fetch_events
from .search.responses import SearchResponse, IndicesInfoResponse, SuggestionResponse

from .service.feed import create_feed, FeedType


class Search(Resource):
    def post(self):
        page = 0
        if len(request.data) == 0:
            result = client.search_all()
        else:
            body = request.get_json()
            if "page" in body:
                page = body["page"]
            result = client.search_all(request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class SearchDataServices(Resource):
    def post(self):
        body = request.get_json()

        page = 0
        if body and "page" in body:
            page = body["page"]

        result = client.search_in_index(index=IndicesKey.DATA_SERVICES, request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class SearchInformationModels(Resource):
    def post(self):
        page = 0
        if len(request.data) == 0:
            result = client.search_in_index(index=IndicesKey.INFO_MODEL)
        else:
            body = request.get_json()
            if "page" in body:
                page = body["page"]
            result = client.search_in_index(index=IndicesKey.INFO_MODEL, request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class SearchDataSet(Resource):
    def get(self) -> Response:
        mimetype = request.accept_mimetypes.best

        if mimetype == "application/rss+xml":
            return Response(response=create_feed(FeedType.RSS), mimetype=mimetype)

        if mimetype == "application/atom+xml":
            return Response(response=create_feed(FeedType.ATOM), mimetype=mimetype)

        return abort(http_status_code=415, description="Unsupported media type")

    def post(self):
        page = 0
        if len(request.data) == 0:
            result = client.search_in_index(index=IndicesKey.DATA_SETS)
        else:
            body = request.get_json()
            if "page" in body:
                page = body["page"]
            result = client.search_in_index(index=IndicesKey.DATA_SETS, request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class SearchConcepts(Resource):
    def post(self):
        page = 0
        if len(request.data) == 0:
            result = client.search_in_index(index=IndicesKey.CONCEPTS)
        else:
            body = request.get_json()
            if "page" in body:
                page = body["page"]
            result = client.search_in_index(index=IndicesKey.CONCEPTS, request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class SearchPublicServices(Resource):
    def post(self):
        page = 0
        if len(request.data) == 0:
            result = client.search_in_index(index=IndicesKey.PUBLIC_SERVICES)
        else:
            body = request.get_json()
            if "page" in body:
                page = body["page"]
            result = client.search_in_index(index=IndicesKey.PUBLIC_SERVICES, request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class SearchEvents(Resource):
    def post(self):
        page = 0
        if len(request.data) == 0:
            result = client.search_in_index(index=IndicesKey.EVENTS)
        else:
            body = request.get_json()
            if "page" in body:
                page = body["page"]
            result = client.search_in_index(index=IndicesKey.EVENTS, request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class SearchPublicServicesAndEvents(Resource):
    def post(self):
        page = 0
        if len(request.data) == 0:
            result = client.search_public_services_and_events()
        else:
            body = request.get_json()
            if "page" in body:
                page = body["page"]
            result = client.search_public_services_and_events(request=body)
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(es_result=result, requested_page=page)


class Count(Resource):
    def get(self):
        return client.count()


class Indices(Resource):
    update_fun = {
        'datasets': fetch_data_sets,
        'informationmodels': fetch_information_models,
        'dataservices': fetch_data_services,
        'concepts': fetch_concepts,
        'all': fetch_all_content,
        'public_services': fetch_public_services,
        "events": fetch_events,
    }

    def get(self):
        """Get information about specific index or all indices"""

        index_name = request.args.get('name')
        if index_name:
            if index_name not in [IndicesKey.INFO_MODEL, IndicesKey.DATA_SERVICES, IndicesKey.DATA_SETS,
                                  IndicesKey.CONCEPTS, IndicesKey.PUBLIC_SERVICES, IndicesKey.EVENTS]:
                abort(http_status_code=400,
                      description={"bad request": "indices '{0}' is not a valid index. Valid indices values are ["
                                                  "datasets,dataservices,informationmodels,concepts]".format(
                          index_name)})
        es_result = client.get_indices(index_name)
        if not es_result:
            abort(http_status_code=404,
                  description="Could not find any information about indices. Try reindexing to update info")
        if es_result['hits']['total']['value'] == 0:
            abort(http_status_code=404,
                  description="Index '{0}' has been removed. Perform request to recreate indices: POST "
                              "/indices?name={0}".format(index_name))
        return IndicesInfoResponse(es_result).map_response()

    def post(self):
        api_key = request.headers.get('X-API-KEY')
        if not api_key or os.getenv("API_KEY", "test-key") != api_key:
            abort(http_status_code=403, description="Forbidden")

        index_name = request.args.get('name')
        if index_name:
            if index_name not in [IndicesKey.INFO_MODEL, IndicesKey.DATA_SERVICES, IndicesKey.DATA_SETS,
                                  IndicesKey.CONCEPTS, IndicesKey.PUBLIC_SERVICES, IndicesKey.EVENTS]:
                abort(http_status_code=400, description="bad request: indices {0} does not exist".format(index_name))
        else:
            index_name = 'all'
        result = self.update_fun[index_name]()
        if result['status'] == 'OK':
            return Response(response=json.dumps(result), status=201, mimetype='application/json')
        else:
            return abort(http_status_code=500, description=result)


class Ping(Resource):
    def get(self):
        client.count()
        return {}


class Ready(Resource):
    def get(self):
        client.count()
        return {}


class Recent(Resource):
    def get(self):
        args = request.args
        size = 5
        if "size" in args:
            size = args["size"]
        result = client.get_recent(size=size)
        return SearchResponse().map_response(es_result=result)


class Suggestion(Resource):
    def get(self, content_type):
        if content_type not in (
        IndicesKey.DATA_SETS, IndicesKey.CONCEPTS, IndicesKey.DATA_SERVICES, IndicesKey.INFO_MODEL):
            abort(http_status_code=400,
                  description="{0} is not a valid content type. Valid content types are [datasets, informationmodels, "
                              "dataservices, concepts]".format(content_type))
        args = request.args
        if "q" in args and len(args["q"]) < 2:
            return SuggestionResponse.empty_response()
        if "lang" in args:
            # TODO
            # return response.map_response(language=args["lang"])
            abort(http_status_code=501,
                  description="fulltext-search does not yet support autocomplete search for specific language")

        result = client.get_suggestions(search_string=args["q"], index_key=content_type)
        response = SuggestionResponse(es_result=result)
        return response.map_response()


class SuggestionAllIndices(Resource):
    def get(self):
        abort(http_status_code=501,
              description="fulltext-search does not yet support autocomplete search for all content")
