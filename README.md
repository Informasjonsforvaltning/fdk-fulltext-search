fdk-fulltext-search
---------------------

##Developing
### Set up virtual environment
```
% pyenv install 3.8.2
% cd <project dir>
% pyenv virtualenv 3.8.2 fdk-fulltext-search # create development environment
% pyenv local fdk-fulltext-search
```
### Install software
```
% pip install pipenv    # package management tool
% pip install invoke    # a task execution tool & library
% pip install pytest    # test framework
% pipenv install --dev  # install packages form Pipfile including dev
```
### Run tests
```
% invoke unit-test
```
```
% invoke contract-tests
```
### Running the service locally
```
% FLASK_APP=src FLASK_ENV=development flask run
```
### Running the service in a wsgi-server (gunicorn)
```
% gunicorn "src:create_app()"  --config=dataservicecatalog/gunicorn_config.py
```
