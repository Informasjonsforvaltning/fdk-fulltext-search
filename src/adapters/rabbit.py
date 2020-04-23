import json
import logging
import os
import time
from json import JSONDecodeError

import pika
from multiprocessing import Process
from pika.adapters.utils.connection_workflow import AMQPConnectorSocketConnectError
from pika.exceptions import AMQPError, StreamLostError, AMQPConnectionError
from src.ingest import fetch_information_models, fetch_data_sets, fetch_data_services, fetch_concepts, \
    fetch_all_content, reindex

queue = "harvester.UpdateSearchTrigger"

user_name = os.getenv("RABBIT_USERNAME") or "admin"
password = os.getenv("RABBIT_PASSWORD") or "admin"
host = os.getenv("RABBIT_HOST") or "localhost"

update_fun = {
    'datasets': fetch_data_sets,
    'informationmodels': fetch_information_models,
    'dataservices': fetch_data_services,
    'concepts': fetch_concepts,
    'all': fetch_all_content
}


class UpdateConsumer:

    def __init__(self):
        consumer_process = Process(target=self.start_listener)
        consumer_process.start()

    def callback(self, ch, method, properties, body):
        logging.info("[rabbitmq]Received msg from queue:\n {0}".format(body))
        try:
            update_type = json.loads(body)["updatesearch"]
            update_with = update_fun[update_type]
            if update_with:
                result = update_with(re_index=True)
                logging.info("[rabbitmq]Result: {0}".format(result))
        except KeyError:
            logging.error("[rabbitmq]Error: Received invalid operation type:\n {0}".format(update_type))
        except JSONDecodeError:
            logging.error("[rabbitmq]Error: Received invalid JSON :\n {0}".format(body))

    def start_listener(self):
        channel = None
        connected = False
        while not connected:
            try:
                logging.info("[rabbitmq] Connection established")
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
