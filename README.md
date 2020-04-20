fdk-fulltext-search
---------------------

## Developing
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
% pipenv install --dev  # install packages from Pipfile including dev
```
#### Env variables:
```
ELASTIC_HOST=localhost
ELASTIC_PORT=9200
ELASTIC_TCP_PORT=9300
RABBIT_HOST=localhost
RABBIT_USERNAME=admin
RABBIT_PASSWORD=admin
API_URL=http://localhost:8080/                  
```

### Running the service locally

```
% docker-comopose up -d                             # start es, rabbitmq and mockserver containers
% pipenv shell                                      # open a session in the virtual environment
% FLASK_APP=src FLASK_ENV=development flask run     # run application
```
### Running the service in a wsgi-server (gunicorn)
```
pipenv shell 
% gunicorn "src:create_app()"  --config=src/gunicorn_config.py --worker-class gevent
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
2. Start a wiremock instance start [record and playback](http://wiremock.org/docs/record-playback/) with target url 
3. Start the application and run an http request to PUT /update
4. copy files from the wiremock instance's /mappings directory into mock_mappings/mappings

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