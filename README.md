fdk-fulltext-search
---------------------

##Developing
Running the service locally
```
FLASK_APP=src FLASK_ENV=development flask run 
```
Running the service in a wsgi-server (gunicorn)
```
gunicorn "src:create_app()"  --config=dataservicecatalog/gunicorn_config.py
```
##Test
```
invoke unit-test
```
```
invoke contract-tests
```