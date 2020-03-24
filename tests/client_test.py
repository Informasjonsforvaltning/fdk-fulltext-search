import pytest
from src.search.client import search_all
from src.search.queries import all_indices, add_aggregation


@pytest.fixture
def mock_elastic(mocker):
    return mocker.patch('elasticsearch.Elasticsearch.search')


@pytest.mark.unit
def test_should_call_search_with_match_all_query(mock_elastic):
    search_all(query_string="")
    mock_elastic.assert_called_once_with(body=add_aggregation(all_indices))

