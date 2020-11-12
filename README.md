fdk-fulltext-search
---------------------


## Developing
### Requirements
```
### Setup envronment 
% pyenv install 3.8.6
% pyenv local 3.8.6
% pip install pipenv==2018.11.26    # package management tool
% pip install invoke    # a task execution tool & library
% pipenv --python 3.8.6 install --dev  # install packages from Pipfile including dev
```
#### Env variables:
```
ELASTIC_HOST=localhost
ELASTIC_PORT=9200
ELASTIC_TCP_PORT=9300
API_URL=http://localhost:8080/
DATASET_HARVESTER_BASE_URI=http://localhost:8080/dataset
ORGANIZATION_CATALOGUE_BASE_URI=http://localhost:8080
REFERENCE_DATA_BASE_URI=http://localhost:8080/reference-data
FDK_SERVICE_HARVESTER_URI=http://localhost:8080
```

### Running the service locally

```
% docker-compose up -d                             # start es, rabbitmq and mockserver containers
% pipenv shell                                      # open a session in the virtual environment
% FLASK_APP=src FLASK_ENV=development flask run     # run application
```
### Running the service in a wsgi-server (gunicorn)
```
pipenv shell 
% gunicorn "src:create_app()"  --config=src/gunicorn_config.py 
```
## Testing
### Running tests
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
--image: name of the image that should be tested. Defaults to digdir/fulltext-search:latest
```
#### Updating mock data
1. Set API_URL env variable to the url you want to collect mock data from
2. `invoke start-docker --attach`
2. Go to `http://0.0.0.0:8080/__admin/recorder/` and start recording with target url 
3. Start the application and run an http request to POST /indices
4. Stop recording

### Other invoke tasks
```
build-image                 # build docker image
options:
--tags                      # commaseperated list of tags for image        
```

```
stop-docker        #shut down containers used in contracttests
options:
--clean                      #remove associated containers and networks
--remove                     #remove associated containers, networks and images   
```
 
 
## Troubleshooting
### Mac: unknown locale: UTF-8 in Python
`open ~/.bash_profile:`

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
restart terminal