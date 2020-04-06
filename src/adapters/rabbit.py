import json
import logging
import time
import pika
from multiprocessing import Process
from pika.adapters.utils.connection_workflow import AMQPConnectorSocketConnectError
from pika.exceptions import AMQPError, StreamLostError, AMQPConnectionError

from src.ingest import fetch_information_models, fetch_datasets, fetch_dataservices, fetch_concepts, \
    fetch_all_content, create_indices, reindex

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
        print("Received msg from queue:\n {0}".format(body))
        update_type = json.loads(body)["type"]
        try:
            update_with = update_fun[update_type]
            if update_with:
                result = update_with()
                print(result)
        except KeyError:
            print("Error: Received invalid operation type:\n {0}".format(update_type))

    def start_listener(self):
        channel = None
        connected = False
        while not connected:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                channel = connection.channel()
                channel.basic_consume(queue='search',
                                      auto_ack=True,
                                      on_message_callback=self.callback)
                print("rabbitmq: Connection established")
                connected = True
            except (AMQPError, AMQPConnectorSocketConnectError, AMQPConnectionError) as err:
                logging.error("Error in rabbitmqp consumer \n {0}".format(err.args))
                # wait 10 seconds, then retry
                time.sleep(10)

        if channel:
            try:
                channel.start_consuming()
            except StreamLostError:
                logging.error("AMPQ Stream lost, attempting to reconnect")
                self.start_listener()
