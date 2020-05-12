import pytest

from src import IndicesKey
from src.search.client import search_all, AllIndicesQuery, get_recent, RecentQuery, get_indices, count, search_in_index, \
    InformationModelQuery


@pytest.fixture
def mock_elastic(mocker):
    return mocker.patch('elasticsearch.Elasticsearch.search')


@pytest.fixture
def mock_index_false_exists(mocker):
    return mocker.patch('src.ingest.es_client.indices.exists', return_value=False)


@pytest.fixture
def mock_index_true_exists(mocker):
    return mocker.patch('src.ingest.es_client.indices.exists', return_value=True)


@pytest.mark.unit
def test_get_indices_should_have_terms_query(mock_elastic, mock_index_true_exists):
    expected_query = {
        "query": {
            "term": {
                "name": "informationmodels"
            }
        }
    }
    get_indices(index_name="informationmodels")
    mock_elastic.assert_called_once_with(body=expected_query, index='info')


@pytest.mark.unit
def test_get_indices_should_have_match_all_query(mock_elastic, mock_index_true_exists):
    expected_query = {
        "query": {
            "match_all": {}
        }
    }
    get_indices()
    mock_elastic.assert_called_once_with(body=expected_query, index='info')


@pytest.mark.unit
def test_get_indices_should_return_none(mock_elastic, mock_index_false_exists):
    result = get_indices("datsets")
    assert result is None


@pytest.mark.unit
def test_should_call_search_with_match_all_query(mock_elastic):
    search_all()
    expectedQuery = AllIndicesQuery()
    expectedQuery.add_aggs()
    mock_elastic.assert_called_once_with(body=expectedQuery.body, search_type='dfs_query_then_fetch')


@pytest.mark.unit
def test_should_call_search_with_match_all_query_and_filters(mock_elastic):
    filters = {
        "filters": [
            {"accessRights": "PUBLIC"}
        ]
    }
    search_all(filters)
    expectedQuery = AllIndicesQuery(filters=[
        {"accessRights": "PUBLIC"}
    ])
    mock_elastic.assert_called_once_with(body=expectedQuery.body, search_type='dfs_query_then_fetch')


@pytest.mark.unit
def test_should_call_search_with_simple_query_string(mock_elastic):
    expectedQuery = AllIndicesQuery(search_string="barnehage", filters=[{'orgPath': '/KOMMUNE/840029212'}])
    req = {
        "q": "barnehage",
        "filters": [
            {'orgPath': '/KOMMUNE/840029212'}
        ]
    }
    search_all(req)
    mock_elastic.assert_called_once_with(body=expectedQuery.body, search_type='dfs_query_then_fetch')


@pytest.mark.unit
def test_should_call_search_with_recent_query(mock_elastic):
    get_recent()
    expectedQuery = RecentQuery().query
    mock_elastic.assert_called_once_with(body=expectedQuery)


@pytest.mark.unit
def test_should_call_search_with_recent_query_and_size_10(mock_elastic):
    get_recent(size=10)
    expectedQuery = RecentQuery(10).query
    mock_elastic.assert_called_once_with(body=expectedQuery)


@pytest.mark.unit
def test_count_should_call_count_for_all_indices(mock_count_elastic):
    count()
    mock_count_elastic.assert_called_once()
    assert mock_count_elastic.call_args_list[0][1].__len__() == 0


@pytest.mark.unit
def test_count_should_call_count_for_specific_index(mock_count_elastic):
    count(index=IndicesKey.INFO_MODEL)
    mock_count_elastic.assert_called_once_with(index=IndicesKey.INFO_MODEL)


@pytest.mark.unit
def test_search_in_should_search_in_information_models_with_information_model_query(mock_elastic):
    search_in_index(index="informationmodels")
    info_query_body = InformationModelQuery().body
    mock_elastic.assert_called_once_with(index=IndicesKey.INFO_MODEL, body=info_query_body)
