from datetime import datetime

import pytest

from fdk_fulltext_search.ingest import create_index, init_info_doc, update_index_info


def mock_update_by_query_result(m_query_success):
    if m_query_success:
        return {"total": 1}
    else:
        return {"total": 0}


@pytest.fixture
def init_info_mock(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.init_info_doc")


@pytest.fixture
def update_index_info_mock(mocker):
    return mocker.patch("fdk_fulltext_search.ingest.update_index_info")


# es_client.index(index="info", body=init_doc)


@pytest.mark.unit
def test_update_info_should_update_doc(mocker, init_info_mock):
    # if info indices exists and doc with index_name exists
    mocker.patch(
        "fdk_fulltext_search.ingest.es_client.indices.exists", return_value=True
    )
    mock_update_by_query = mocker.patch(
        "fdk_fulltext_search.ingest.es_client.update_by_query",
        return_value=mock_update_by_query_result(True),
    )
    update_index_info(index_name="concept")
    assert init_info_mock.call_count == 0
    assert mock_update_by_query.call_count == 1
    assert (
        mock_update_by_query.call_args[1]["body"]["query"]["term"]["name"] == "concept"
    )


@pytest.mark.unit
def test_update_info_should_init_doc_if_not_found(mocker, init_info_mock):
    # if info indices exists and doc with index_name does not exists
    mocker.patch(
        "fdk_fulltext_search.ingest.es_client.indices.exists", return_value=True
    )
    mock_update_by_query = mocker.patch(
        "fdk_fulltext_search.ingest.es_client.update_by_query",
        return_value=mock_update_by_query_result(False),
    )
    update_index_info(index_name="some_index")
    assert mock_update_by_query.call_count == 1
    assert init_info_mock.call_count == 1


@pytest.mark.unit
def test_init_info_doc_should_create_indices_and_doc(mocker, mock_single_create):
    # if indices does not exist
    mocker.patch(
        "fdk_fulltext_search.ingest.es_client.indices.exists", return_value=False
    )
    mock_index_doc = mocker.patch("fdk_fulltext_search.ingest.es_client.index")
    init_info_doc(index_name="informationmodels", now=datetime.now())
    assert mock_single_create.call_count == 1
    assert mock_single_create.call_args[1]["index"] == "info"
    assert mock_index_doc.call_count == 1
    assert mock_index_doc.call_args[1]["body"]["name"] == "informationmodels"


@pytest.mark.unit
def test_create_index_should_abort_when_new_index_does_not_exist(
    mocker, mock_env, mock_single_create, update_index_info_mock
):
    # if indices does not exist
    mocker.patch(
        "fdk_fulltext_search.ingest.es_client.indices.exists", return_value=False
    )
    create_index(index_alias="dataservices", new_index_name="dataservices-123")
    assert mock_single_create.call_count == 1
    assert mock_single_create.call_args[1]["index"] == "dataservices-123"
    assert update_index_info_mock.call_count == 0


@pytest.mark.unit
def test_create_index_updates_info_index_when_successful(
    mocker, mock_env, mock_single_create, update_index_info_mock
):
    # if indices exist
    mocker.patch(
        "fdk_fulltext_search.ingest.es_client.indices.exists", return_value=True
    )
    create_index(index_alias="dataservices", new_index_name="dataservices-123")
    assert mock_single_create.call_args[1]["index"] == "dataservices-123"
    assert mock_single_create.call_count == 1
    assert mock_single_create.call_args[1]["index"] == "dataservices-123"
    assert update_index_info_mock.call_count == 1
