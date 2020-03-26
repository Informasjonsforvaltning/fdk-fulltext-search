import pytest
from src.search.client import search_all, AllIndicesQuery


@pytest.fixture
def mock_elastic(mocker):
    return mocker.patch('elasticsearch.Elasticsearch.search')


@pytest.mark.unit
def test_should_call_search_with_match_all_query(mock_elastic):
    search_all()
    expectedQuery = AllIndicesQuery()
    expectedQuery.add_aggs()
    mock_elastic.assert_called_once_with(body=expectedQuery.query)

