import os
from flask import Flask
from flask_restful import Api
from .endpoints import *


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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
    api.add_resource(AutoComplete, '/autocomplete')
    api.add_resource(Count, '/count')
    api.add_resource(Harvest, '/harvest')
    return app
