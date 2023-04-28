import os
from typing import Any, Optional

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

import fdk_fulltext_search.endpoints as endpoints


def create_app(test_config: Optional[Any] = None) -> Flask:
    # Create and configure the app
    load_dotenv(override=True)
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
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
    api.add_resource(endpoints.Search, "/search")
    api.add_resource(endpoints.Count, "/count")
    api.add_resource(endpoints.Ping, "/ping")
    api.add_resource(endpoints.Ready, "/ready")
    api.add_resource(endpoints.Recent, "/recent")
    api.add_resource(endpoints.Indices, "/indices")
    api.add_resource(endpoints.SearchInformationModels, "/informationmodels")
    api.add_resource(endpoints.SearchDataSet, "/datasets")
    api.add_resource(endpoints.SearchDataServices, "/dataservices")
    api.add_resource(endpoints.SearchConcepts, "/concepts")
    api.add_resource(endpoints.SearchPublicServices, "/public-services")
    api.add_resource(endpoints.SearchEvents, "/events")
    api.add_resource(
        endpoints.SearchPublicServicesAndEvents, "/public-services-and-events"
    )
    api.add_resource(endpoints.Suggestion, "/suggestion/<string:content_type>")
    api.add_resource(endpoints.SuggestionAllIndices, "/suggestion")

    return app
