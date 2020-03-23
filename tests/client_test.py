import pytest
from src.search.client import search_all
from src.search.queries import match_all


@pytest.fixture
def mock_elastic(mocker):
    return mocker.patch('elasticsearch.Elasticsearch.search')


@pytest.mark.unit
def test_should_call_search_with_match_all_query(mock_elastic):
    search_all(query_string="")
    mock_elastic.assert_called_once_with(body=match_all)

@pytest.mark.unit
def test_should_call_search_with_dismax_query(mock_elastic):
    search_all(query_string="some search string")
    mock_elastic.assert_called_once_with(body={"dismax": {"queries": []}})
