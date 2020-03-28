from flask_restful import Resource
from flask import request
from .search import client
from .ingest import fetch_from_services,create_indices
from .search.responses import SearchResponse


class Search(Resource):
    def post(self):
        if len(request.data) == 0:
            result = client.search_all()
        else:
            result = client.search_all(request=request.get_json())
        return SearchResponse().map_response(result)


class Count(Resource):
    def get(self):
        return client.count()


class Update(Resource):
    def put(self):
        return fetch_from_services()

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
