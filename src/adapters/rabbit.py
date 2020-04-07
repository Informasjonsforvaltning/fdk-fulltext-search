import json
import logging
import os
import time
import pika
from multiprocessing import Process
from pika.adapters.utils.connection_workflow import AMQPConnectorSocketConnectError
from pika.exceptions import AMQPError, StreamLostError, AMQPConnectionError
from src.ingest import fetch_information_models, fetch_datasets, fetch_dataservices, fetch_concepts, \
    fetch_all_content, reindex

queue = "harvester.UpdateSearchTrigger"

user_name = os.getenv("RABBIT_USERNAME") or "admin"
password = os.getenv("RABBIT_PASSWORD") or "admin"
host = os.getenv("RABBIT_HOST") or "localhost"

update_fun = {
    'datasets': fetch_datasets,
    'informationmodels': fetch_information_models,
    'dataservices': fetch_dataservices,
    'concepts': fetch_concepts,
    'all': fetch_all_content,
    'reindex': reindex
}


class UpdateConsumer:

    def __init__(self):
        consumer_process = Process(target=self.start_listener)
        consumer_process.start()

    def callback(self, ch, method, properties, body):
        print("[rabbitmq]Received msg from queue:\n {0}".format(body))
        update_type = json.loads(body)["updatesearch"]
        try:
            update_with = update_fun[update_type]
            if update_with:
                result = update_with()
                print("[rabbitmq]Result: {0}".format(result))
        except KeyError:
            print("[rabbitmq]Error: Received invalid operation type:\n {0}".format(update_type))

    def start_listener(self):
        channel = None
        connected = False
        while not connected:
            try:
                print("[rabbitmq] Connection established")
                credentials = pika.PlainCredentials(username=user_name,
                                                    password=password)

                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=host, credentials=credentials)
                )

                channel = connection.channel()
                channel.basic_consume(queue=queue,
                                      auto_ack=True,
                                      on_message_callback=self.callback)
                connected = True
            except (AMQPError, AMQPConnectorSocketConnectError, AMQPConnectionError) as err:
                logging.error("[rabbitmq]Error in consumer \n {0}".format(err.args))
                # wait 60 seconds, then retry
                time.sleep(60)

        if channel:
            try:
                channel.start_consuming()
            except StreamLostError:
                logging.error("[rabbitmq]AMPQ Stream lost, attempting to reconnect")
                self.start_listener()
