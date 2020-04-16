import json
import os

import pika
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

queue = "harvester.UpdateSearchTrigger"

user_name = os.getenv("RABBIT_USERNAME") or "admin"
password = os.getenv("RABBIT_PASSWORD") or "admin"
host = os.getenv("RABBIT_HOST") or "localhost"


def wait_for_es():
    # wait  for elasticsearch to be ready
    retry_strategy = Retry(connect=5, read=5, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("http://", adapter)
    es_health = http.get("http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s")
    if es_health.status_code != 200:
        raise Exception('Test containers: could not contact ElasticsSearch')
    return


def populate():
    send_rabbitmq_message("reindex")
    timeout = time.time() + 90
    while True:
        response = requests.get("http://localhost:8000/count")
        if response.status_code != 200:
            raise Exception('Test containers: request to service returned ' + response.status_code)
        if response.json()['count'] == 5622:
            break
        if time.time() > timeout:
            raise Exception('Test containers: timed out while waiting for count response, last response was'.format(
                response.content))
        time.sleep(1)


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
