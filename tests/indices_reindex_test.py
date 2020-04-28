import os
from datetime import datetime
from unittest.mock import mock_open

import pytest

from src.ingest import update_index_info, init_info_doc, reindex_specific_index


def mock_update_by_query_result(m_query_success):
    if m_query_success:
        return {"total": 1}
    else:
        return {"total": 0}


@pytest.fixture
def init_info_mock(mocker):
    return mocker.patch("src.ingest.init_info_doc")


@pytest.fixture
def update_index_info_mock(mocker):
    return mocker.patch("src.ingest.update_index_info")


# es_client.index(index="info", body=init_doc)

@pytest.mark.unit
def test_update_info_should_update_doc(mocker, init_info_mock):
    # if info indices exists and doc with index_name exists
    mocker.patch("src.ingest.es_client.indices.exists", return_value=True)
    mock_update_by_query = mocker.patch("src.ingest.es_client.update_by_query",
                                        return_value=mock_update_by_query_result(True))
    update_index_info(index_name="concept")
    assert init_info_mock.call_count == 0
    assert mock_update_by_query.call_count == 1
    assert mock_update_by_query.call_args[1]['body']['query']['term']['name'] == "concept"


@pytest.mark.unit
def test_update_info_should_init_doc_if_not_found(mocker, init_info_mock):
    # if info indices exists and doc with index_name does not exists
    mocker.patch("src.ingest.es_client.indices.exists", return_value=True)
    mock_update_by_query = mocker.patch("src.ingest.es_client.update_by_query",
                                        return_value=mock_update_by_query_result(False))
    update_index_info(index_name="some_index")
    assert mock_update_by_query.call_count == 1
    assert init_info_mock.call_count == 1


@pytest.mark.unit
def test_init_info_doc_should_create_indices_and_doc(mocker, mock_single_create):
    # if indices does not exist
    mocker.patch("src.ingest.es_client.indices.exists", return_value=False)
    mock_index_doc = mocker.patch("src.ingest.es_client.index")
    init_info_doc(index_name="informationmodels", now=datetime.now())
    assert mock_single_create.call_count == 1
    assert mock_single_create.call_args[1]['index'] == "info"
    assert mock_index_doc.call_count == 1
    assert mock_index_doc.call_args[1]['body']['name'] == 'informationmodels'


@pytest.mark.unit
def test_reindex_specific_index_should_create_new_index(mocker,
                                                        mock_env,
                                                        mock_single_create,
                                                        mock_single_delete,
                                                        update_index_info_mock):
    # if indices does not exist
    mocker.patch("src.ingest.es_client.indices.exists", return_value=False)
    reindex_specific_index(index_name="dataservices")
    assert mock_single_delete.call_count == 0
    assert mock_single_create.call_count == 1
    assert mock_single_create.call_args[1]['index'] == "dataservices"
    assert update_index_info_mock.call_count == 1


@pytest.mark.unit
def test_reindex_specific_index_should_delete_and_create_new_index(mocker,
                                                                   mock_env,
                                                                   mock_single_create,
                                                                   mock_single_delete,
                                                                   update_index_info_mock):
    # if indices exist
    mocker.patch("src.ingest.es_client.indices.exists", return_value=True)
    reindex_specific_index(index_name="dataservices")
    assert mock_single_create.call_args[1]['index'] == "dataservices"
    assert mock_single_delete.call_count == 1
    assert mock_single_create.call_count == 1
    assert mock_single_create.call_args[1]['index'] == "dataservices"
    assert update_index_info_mock.call_count == 1
