fdk-fulltext-search
---------------------


## Developing
### Requirements
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Install software:
```
% pip install poetry==1.1.4
% pip install nox==2020.12.31
% pip install nox-poetry==0.8.1
% poetry install
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
FDK_EVENT_HARVESTER_URI=http://localhost:8080
```

### Running the service locally

```
% docker-compose up -d
% poetry shell
% FLASK_APP=fdk_fulltext_search FLASK_ENV=development ORGANIZATION_CATALOGUE_BASE_URI=http://localhost:8080 REFERENCE_DATA_BASE_URI=http://localhost:8080/reference-data flask run --port=5000
```
## Testing
### Running tests
#### All tests
```
% nox
```
#### Unit tests
```
% nox -s unit_tests
```
#### Contract tests
```
% nox -s contract_tests
```
#### Updating mock data
1. Set API_URL env variable to the url you want to collect mock data from
2. `invoke start-docker --attach`
2. Go to `http://0.0.0.0:8080/__admin/recorder/` and start recording with target url
3. Start the application and run an http request to POST /indices
4. Stop recording

### Other helpful commands

Code formatting:
```
% nox -s black
```

Run tests outside of a nox session:
```
% poetry run pytest
```

Run specific nox sessions:
```
% nox -s safety
% nox -rs lint
```

Run session with specified arguments:
```
% nox -s tests -- -vv
```

