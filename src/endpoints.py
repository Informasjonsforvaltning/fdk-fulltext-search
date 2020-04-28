import json

from flask_restful import Resource, reqparse, abort
from flask import request, Response, jsonify
from .search import client
from .ingest import fetch_all_content, reindex_all_indices, IndicesKey, fetch_data_sets, fetch_information_models, \
    fetch_data_services, fetch_concepts, reindex
from .search.responses import SearchResponse, IndicesInfoResponse


class Search(Resource):
    def post(self):
        if len(request.data) == 0:
            result = client.search_all()
        else:
            result = client.search_all(request=request.get_json())
        if "error" in result.keys():
            return result
        else:
            return SearchResponse().map_response(result)


class Count(Resource):
    def get(self):
        return client.count()


class Update(Resource):
    def put(self):
        return fetch_all_content()

    def delete(self):
        reindex_all_indices()


class Indices(Resource):
    update_fun = {
        'datasets': fetch_data_sets,
        'informationmodels': fetch_information_models,
        'dataservices': fetch_data_services,
        'concepts': fetch_concepts,
        'all': fetch_all_content,
    }

    def get(self):
        """Get information about specific index or all indices"""

        index_name = request.args.get('name')
        if index_name:
            if index_name not in [IndicesKey.INFO_MODEL, IndicesKey.DATA_SERVICES, IndicesKey.DATA_SETS,
                                  IndicesKey.CONCEPTS]:
                abort(http_status_code=400,
                      description={"bad request": "indices '{0}' is not a valid index. Valid indices values are ["
                                                  "datasets,dataservices,informationmodels,concepts]".format(index_name)})
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
        index_name = request.args.get('name')
        if index_name:
            if index_name not in [IndicesKey.INFO_MODEL, IndicesKey.DATA_SERVICES, IndicesKey.DATA_SETS,
                                  IndicesKey.CONCEPTS]:
                abort(http_status_code=400, description="bad request: indices {0} does not exist".format(index_name))
        else:
            index_name = 'all'
        result = self.update_fun[index_name](re_index=True)
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
