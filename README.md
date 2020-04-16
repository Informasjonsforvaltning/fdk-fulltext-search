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
### Running the service locally
```
% FLASK_APP=src FLASK_ENV=development flask run
```
### Running the service in a wsgi-server (gunicorn)
```
% gunicorn "src:create_app()"  --config=dataservicecatalog/gunicorn_config.py
```

### Run tests
```
% invoke unit-test

options:
--install: install pip-dependencies, used by github actions
```
```
% invoke contract-test 
options:
--build: build image for testing before run
--compose: start docker compose for testing before run
```

#### Updating mock data
1. Set API_URL env variable to the url you want to collect mock data from
2. Start a wiremock instance start [record and playback](http://wiremock.org/docs/record-playback/) with target url 
3. Start the application and run an http request to PUT /update
4. copy files from the wirmock instance's /mappings directory into mock_mappings/mappings
 
### Troubleshooting
#### Mac: unknown locale: UTF-8 in Python
`open ~/.bash_profile:`

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
restart terminal