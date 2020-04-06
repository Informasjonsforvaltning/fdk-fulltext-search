import json
from unittest import mock
import pika
import pytest

from src.adapters.rabbit import queue, user_name, password, host


def send_message(data_type):
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


@mock.patch('src.ingest.fetch_information_models')
@pytest.mark.integration
def test_should_start_update_of_informationmodels(mock):
    send_message("informationmodels")
    mock.assert_called()


@mock.patch('src.ingest.fetch_concepts')
@pytest.mark.integration
def test_should_start_update_of_concepts(mock):
    send_message("concepts")
    mock.assert_called()


@mock.patch('src.ingest.fetch_dataservices')
@pytest.mark.integration
def test_should_start_update_of_dataservices(mock):
    send_message("dataservices")
    mock.assert_called()


@mock.patch('src.ingest.fetch_datasets')
@pytest.mark.integration
def test_should_start_update_of_datasets(mock):
    send_message("datasets")
    mock.assert_called()


@mock.patch('src.ingest.fetch_datasets')
@pytest.mark.integration
def test_delete_all_data(mock):
    send_message("reindex")
    mock.assert_called()
