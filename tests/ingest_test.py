import pytest

from src.ingest import fetch_information_models, fetch_concepts, fetch_data_sets, fetch_data_services, \
    reindex_specific_index


@pytest.mark.unit
def test_fetch_info_models_should_initiate_reindex(mock_env, mock_ingest, mock_get, mock_single_reindex):
    fetch_information_models(re_index=True)
    assert mock_single_reindex.call_count == 1
    assert mock_single_reindex.call_args_list[0][0][0] == 'informationmodels'
    assert mock_ingest.call_count == 1
    ingest_calls = mock_ingest.call_args_list[0][0]
    assert ingest_calls[1] == 'informationmodels'
    assert ingest_calls[2] == 'id'



@pytest.mark.unit
def test_fetch_info_models_should_not_initiate_reindex(mock_env, mock_get, mock_ingest, mock_single_reindex):
    fetch_information_models()
    assert mock_ingest.call_count == 1
    ingest_calls = mock_ingest.call_args_list[0][0]
    assert ingest_calls[1] == 'informationmodels'
    assert ingest_calls[2] == 'id'
    assert mock_single_reindex.call_count == 0


@pytest.mark.unit
def test_fetch_concepts_should_initiate_reindex(mock_env, mock_ingest, mock_get, mock_single_reindex):
    fetch_concepts(re_index=True)
    assert mock_ingest.call_count == 1
    ingest_calls = mock_ingest.call_args_list[0][0]
    assert ingest_calls[1] == 'concepts'
    assert ingest_calls[2] == 'id'
    assert mock_single_reindex.call_count == 1
    assert mock_single_reindex.call_args_list[0][0][0] == 'concepts'


@pytest.mark.unit
def test_fetch_concepts_should_not_initiate_reindex(mock_env, mock_get, mock_ingest, mock_single_reindex):
    fetch_concepts()
    assert mock_ingest.call_count == 1
    ingest_calls = mock_ingest.call_args_list[0][0]
    assert ingest_calls[1] == 'concepts'
    assert ingest_calls[2] == 'id'
    assert mock_single_reindex.call_count == 0


@pytest.mark.unit
def test_fetch_data_services_should_initiate_reindex(mock_env, mock_ingest, mock_get, mock_single_reindex):
    fetch_data_services(re_index=True)
    assert mock_ingest.call_count == 1
    ingest_calls = mock_ingest.call_args_list[0][0]
    assert ingest_calls[1] == 'dataservices'
    assert ingest_calls[2] == 'id'
    assert mock_single_reindex.call_count == 1
    assert mock_single_reindex.call_args_list[0][0][0] == 'dataservices'


@pytest.mark.unit
def test_fetch_data_services_should_not_initiate_reindex(mock_env, mock_get, mock_ingest, mock_single_reindex):
    fetch_data_services()
    assert mock_ingest.call_count == 1
    ingest_calls = mock_ingest.call_args_list[0][0]
    assert ingest_calls[1] == 'dataservices'
    assert ingest_calls[2] == 'id'
    assert mock_single_reindex.call_count == 0


@pytest.mark.unit
def test_fetch_datasets_should_initiate_reindex(mock_env, mock_ingest_from_source, mock_get, mock_single_reindex):
    fetch_data_sets(re_index=True)
    assert mock_ingest_from_source.call_count == 1
    ingest_calls = mock_ingest_from_source.call_args_list[0][0]
    assert ingest_calls[1] == 'datasets'
    assert ingest_calls[2] == '_id'
    assert mock_single_reindex.call_count == 1
    assert mock_single_reindex.call_args_list[0][0][0] == 'datasets'


@pytest.mark.unit
def test_fetch_datasets_should_not_initiate_reindex(mock_env, mock_get, mock_ingest_from_source, mock_single_reindex):
    fetch_data_sets()
    assert mock_ingest_from_source.call_count == 1
    ingest_calls = mock_ingest_from_source.call_args_list[0][0]
    assert ingest_calls[1] == 'datasets'
    assert ingest_calls[2] == '_id'
    assert mock_single_reindex.call_count == 0




