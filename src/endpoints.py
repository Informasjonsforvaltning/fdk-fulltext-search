from flask_restful import Resource
from .search import client
from .ingest import fetch_information_models, fetch_concepts, fetch_dataservices, fetch_datasets


class Search(Resource):
    def post(self):
        result = client.search_all("")
        return result


class AutoComplete(Resource):
    def post(self):
        return {"hello": "autocomplete"}


class Count(Resource):
    def get(self):
        return client.count()


class Harvest(Resource):
    def post(self):
        fetch_information_models()
        fetch_concepts()
        fetch_dataservices()
        fetch_datasets()
        return {"status": "successfull"}
