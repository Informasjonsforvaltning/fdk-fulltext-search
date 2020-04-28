import pytest
from src.search.client import search_all, AllIndicesQuery, get_recent, RecentQuery


@pytest.fixture
def mock_elastic(mocker):
    return mocker.patch('elasticsearch.Elasticsearch.search')


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
