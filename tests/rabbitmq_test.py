import json
from unittest import mock
import pika
import pytest


def send_message(data_type):
    msg = json.dumps({
        "type": data_type,
        "update_content": "all"
    })
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='search')
    channel.basic_publish(exchange='',
                          routing_key='search',
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
