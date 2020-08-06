import json
import logging
import os
import time
from json import JSONDecodeError
from multiprocessing import Process

import pika
from pika.adapters.utils.connection_workflow import AMQPConnectorSocketConnectError
from pika.exceptions import AMQPError, StreamLostError, AMQPConnectionError

from src.ingest import (
    fetch_information_models,
    fetch_data_sets,
    fetch_data_services,
    fetch_concepts,
    fetch_all_content
)

user_name = os.getenv("RABBIT_USERNAME", "admin")
password = os.getenv("RABBIT_PASSWORD", "admin")
host = os.getenv("RABBIT_HOST", "localhost")

update_fun = {
    'dataset': fetch_data_sets,
    'informationmodel': fetch_information_models,
    'dataservice': fetch_data_services,
    'concept': fetch_concepts,
    'all': fetch_all_content,
}


class UpdateConsumer:

    def __init__(self):
        consumer_process = Process(target=self.start_listener)
        consumer_process.start()

    @staticmethod
    def callback(ch, method, properties, body):
        routing_key = method.routing_key
        logging.info(f"[rabbitmq]Received msg from {routing_key}:\n {body}")
        try:
            update_type = routing_key.split('.')[0]
            update_with = update_fun[update_type]

            if update_with:
                body = json.loads(body)
                identifier = body['identifier'] if 'identifier' in body else None

                if update_type == 'all':
                    result = update_with(re_index=True)
                else:
                    result = update_with(identifier=identifier, re_index=True)

                logging.info(f"[rabbitmq]Result: {result}")
                return result

        except KeyError:
            logging.error(f"[rabbitmq]Error: Received invalid operation type: {routing_key}")
        except JSONDecodeError:
            logging.error(f"[rabbitmq]Error: Received invalid JSON :\n {body}")

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

                channel.exchange_declare(exchange='harvests', exchange_type='topic')

                result = channel.queue_declare('', exclusive=True, auto_delete=True)
                queue_name = result.method.queue

                channel.queue_bind(exchange='harvests', queue=queue_name, routing_key='*.harvester.UpdateSearchTrigger')

                channel.basic_consume(queue=queue_name,
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
