import pytest

from fdk_fulltext_search.ingest import (
    fetch_concepts,
    fetch_data_services,
    fetch_data_sets,
    fetch_events,
    fetch_information_models,
    fetch_public_services,
    PipelinesKey,
)


@pytest.mark.unit
def test_fetch_info_models_should_create_index_and_update_alias(
    mock_env,
    mock_ingest_from_harvester,
    mock_get,
    mock_single_reindex,
    mock_set_alias,
    mock_model_parser,
):
    fetch_information_models()
    assert mock_ingest_from_harvester.call_count == 1
    ingest_calls = mock_ingest_from_harvester.call_args_list[0][0]
    assert "informationmodels-" in ingest_calls[1]
    assert ingest_calls[2] == "id"
    assert mock_single_reindex.call_count == 1
    create_calls = mock_single_reindex.call_args_list[0][0]
    assert create_calls[0] == "informationmodels"
    assert "informationmodels-" in create_calls[1]
    assert mock_set_alias.call_count == 1
    alias_calls = mock_set_alias.call_args_list[0][0]
    assert alias_calls[0] == "informationmodels"
    assert "informationmodels-" in alias_calls[1]


@pytest.mark.unit
def test_fetch_concepts_should_create_index_and_update_alias(
    mock_env, mock_ingest_from_harvester, mock_get, mock_single_reindex, mock_set_alias
):
    fetch_concepts()
    assert mock_ingest_from_harvester.call_count == 1
    ingest_calls = mock_ingest_from_harvester.call_args_list[0][0]
    assert "concepts-" in ingest_calls[1]
    assert ingest_calls[2] == "id"
    assert mock_single_reindex.call_count == 1
    create_calls = mock_single_reindex.call_args_list[0][0]
    assert create_calls[0] == "concepts"
    assert "concepts-" in create_calls[1]
    assert mock_set_alias.call_count == 1
    alias_calls = mock_set_alias.call_args_list[0][0]
    assert alias_calls[0] == "concepts"
    assert "concepts-" in alias_calls[1]


@pytest.mark.unit
def test_fetch_data_services_should_create_index_and_update_alias(
    mock_env,
    mock_create_or_update_dataservice_pipeline,
    mock_ingest_from_harvester,
    mock_get,
    mock_single_reindex,
    mock_set_alias,
    mock_data_service_parser,
):
    fetch_data_services()
    assert mock_create_or_update_dataservice_pipeline.call_count == 1
    pipeline_calls = mock_create_or_update_dataservice_pipeline.call_args_list[0][0]
    assert pipeline_calls[0] == PipelinesKey.DATA_SERVICES
    assert mock_ingest_from_harvester.call_count == 1
    ingest_calls = mock_ingest_from_harvester.call_args_list[0][0]
    assert "dataservices-" in ingest_calls[1]
    assert ingest_calls[2] == "id"
    assert ingest_calls[3] == PipelinesKey.DATA_SERVICES
    assert mock_single_reindex.call_count == 1
    create_calls = mock_single_reindex.call_args_list[0][0]
    assert create_calls[0] == "dataservices"
    assert "dataservices-" in create_calls[1]
    assert mock_set_alias.call_count == 1
    alias_calls = mock_set_alias.call_args_list[0][0]
    assert alias_calls[0] == "dataservices"
    assert "dataservices-" in alias_calls[1]


@pytest.mark.unit
def test_fetch_datasets_should_create_index_and_update_alias(
    mock_env,
    mock_create_or_update_dataset_pipeline,
    mock_ingest_from_harvester,
    mock_get,
    mock_single_reindex,
    mock_set_alias,
    mock_dataset_parser,
):
    fetch_data_sets()
    assert mock_create_or_update_dataset_pipeline.call_count == 1
    pipeline_calls = mock_create_or_update_dataset_pipeline.call_args_list[0][0]
    assert pipeline_calls[0] == PipelinesKey.DATA_SETS
    assert mock_ingest_from_harvester.call_count == 1
    ingest_calls = mock_ingest_from_harvester.call_args_list[0][0]
    assert "datasets-" in ingest_calls[1]
    assert ingest_calls[2] == "_id"
    assert ingest_calls[3] == PipelinesKey.DATA_SETS
    assert mock_single_reindex.call_count == 1
    create_calls = mock_single_reindex.call_args_list[0][0]
    assert create_calls[0] == "datasets"
    assert "datasets-" in create_calls[1]
    assert mock_set_alias.call_count == 1
    alias_calls = mock_set_alias.call_args_list[0][0]
    assert alias_calls[0] == "datasets"
    assert "datasets-" in alias_calls[1]


@pytest.mark.unit
def test_fetch_public_services_should_create_index_and_update_alias(
    mock_env,
    mock_ingest_from_harvester,
    mock_get,
    mock_single_reindex,
    mock_set_alias,
    mock_dataset_parser,
):
    fetch_public_services()
    assert mock_ingest_from_harvester.call_count == 1
    ingest_calls = mock_ingest_from_harvester.call_args_list[0][0]
    assert "public_services-" in ingest_calls[1]
    assert ingest_calls[2] == "id"
    assert mock_single_reindex.call_count == 1
    create_calls = mock_single_reindex.call_args_list[0][0]
    assert create_calls[0] == "public_services"
    assert "public_services-" in create_calls[1]
    assert mock_set_alias.call_count == 1
    alias_calls = mock_set_alias.call_args_list[0][0]
    assert alias_calls[0] == "public_services"
    assert "public_services-" in alias_calls[1]


@pytest.mark.unit
def test_fetch_events_should_create_index_and_update_alias(
    mock_env,
    mock_ingest_from_harvester,
    mock_get,
    mock_single_reindex,
    mock_set_alias,
    mock_dataset_parser,
):
    fetch_events()
    assert mock_ingest_from_harvester.call_count == 1
    ingest_calls = mock_ingest_from_harvester.call_args_list[0][0]
    assert "events-" in ingest_calls[1]
    assert ingest_calls[2] == "id"
    assert mock_single_reindex.call_count == 1
    create_calls = mock_single_reindex.call_args_list[0][0]
    assert create_calls[0] == "events"
    assert "events-" in create_calls[1]
    assert mock_set_alias.call_count == 1
    alias_calls = mock_set_alias.call_args_list[0][0]
    assert alias_calls[0] == "events"
    assert "events-" in alias_calls[1]
