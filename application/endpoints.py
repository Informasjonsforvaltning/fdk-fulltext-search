from flask_restful import Resource
from .search import client


class Search(Resource):
    def post(self):
        result = client.search_all("")
        return {"hello": result}


class AutoComplete(Resource):
    def post(self):
        return {"hello": "autocomplete"}


class ApplicationStatus(Resource):
    def get(self):
        return {"item count": client.count()}
