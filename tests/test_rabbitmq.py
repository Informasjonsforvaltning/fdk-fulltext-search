from unittest import mock

import pytest

from tests.contract.contract_utils import send_rabbitmq_message


# def send_message(data_type):
#     msg = json.dumps({
#         "updatesearch": data_type
#     })
#     credentials = pika.PlainCredentials(username=user_name,
#                                         password=password)
#
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host=host, credentials=credentials)
#     )
#     channel = connection.channel()
#     channel.queue_declare(queue=queue)
#     channel.basic_publish(exchange='',
#                           routing_key=queue,
#                           body=msg)
#     connection.close()


@mock.patch('src.ingest.fetch_information_models')
@pytest.mark.integration
def test_should_start_update_of_informationmodels(mock):
    send_rabbitmq_message("informationmodel")
    mock.assert_called()


@mock.patch('src.ingest.fetch_concepts')
@pytest.mark.integration
def test_should_start_update_of_concepts(mock):
    send_rabbitmq_message("concept")
    mock.assert_called()


@mock.patch('src.ingest.fetch_dataservices')
@pytest.mark.integration
def test_should_start_update_of_dataservices(mock):
    send_rabbitmq_message("dataservice")
    mock.assert_called()


@mock.patch('src.ingest.fetch_datasets')
@pytest.mark.integration
def test_should_start_update_of_datasets(mock):
    send_rabbitmq_message("dataset")
    mock.assert_called()

# TODO: in order to add support for reindex, add field in message body next to "identifier"
# TODO: like {"reindex": true}

# @mock.patch('src.ingest.fetch_datasets')
# @pytest.mark.integration
# def test_delete_all_data(mock):
#     send_message("reindex")
#     mock.assert_called()
