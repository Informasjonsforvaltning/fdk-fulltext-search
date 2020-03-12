import os
from elasticsearch_dsl import connections

elasticHost = os.getenv('ELASTIC_HOST')
connections.configure(default={'hosts': elasticHost})
