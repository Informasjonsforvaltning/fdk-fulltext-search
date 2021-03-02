from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from src.fdk_fulltext_search.endpoints import *


def create_app(test_config=None):

    # Create and configure the app
    load_dotenv(override=True)
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # add endpoints
    api = Api(app)
    api.add_resource(Search, '/search')
    api.add_resource(Count, '/count')
    api.add_resource(Ping, '/ping')
    api.add_resource(Ready, '/ready')
    api.add_resource(Recent, '/recent')
    api.add_resource(Indices, '/indices')
    api.add_resource(SearchInformationModels, '/informationmodels')
    api.add_resource(SearchDataSet, '/datasets')
    api.add_resource(SearchDataServices, '/dataservices')
    api.add_resource(SearchConcepts, '/concepts')
    api.add_resource(SearchPublicServices, '/public-services')
    api.add_resource(SearchEvents, '/events')
    api.add_resource(SearchPublicServicesAndEvents, '/public-services-and-events')
    api.add_resource(Suggestion, '/suggestion/<string:content_type>')
    api.add_resource(SuggestionAllIndices, '/suggestion')

    return app
