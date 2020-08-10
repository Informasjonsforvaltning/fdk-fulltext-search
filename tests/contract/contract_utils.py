import json
import os
import time

import pika
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import NewConnectionError, MaxRetryError
from urllib3.util.retry import Retry

queue = "harvester.UpdateSearchTrigger"

user_name = os.getenv("RABBIT_USERNAME", "admin")
password = os.getenv("RABBIT_PASSWORD", "admin")
host = os.getenv("RABBIT_HOST", "localhost")

expected_content_keys = ["hits", "page", "aggregations"]
expected_page_keys = ["totalElements", "totalPages", "currentPage", "size"]


def wait_for_es():
    # wait  for elasticsearch to be ready
    try:
        retry_strategy = Retry(connect=2, read=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("http://", adapter)
        es_health = http.get("http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s")
        if es_health.status_code != 200:
            pytest.fail('Test containers: could not contact ElasticSearch')
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test containers: could not contact ElasticsSearch')
    return


def populate():
    send_rabbitmq_message("all")
    timeout = time.time() + 90
    try:
        while True:
            response = requests.get("http://localhost:8000/count")
            if response.json()['count'] >= 5569:
                break
            if time.time() > timeout:
                pytest.fail('Test containers: timed out while waiting for poupulation of ElasticSearch, last response '
                            'was {0}'.format(response.json()["count"]))
            time.sleep(1)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError):
        pytest.fail('Test containers: could not contact fdk-fulltext-search container')


def send_rabbitmq_message(data_type):
    msg = json.dumps({
        "updatesearch": data_type
    })
    credentials = pika.PlainCredentials(username=user_name,
                                        password=password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=msg)
    connection.close()
    time.sleep(2)
