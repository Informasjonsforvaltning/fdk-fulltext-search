from flask_restful import Resource, reqparse
from flask import request
from .search import client
from .ingest import fetch_all_content, create_indices
from .search.responses import SearchResponse


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
        create_indices()


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
