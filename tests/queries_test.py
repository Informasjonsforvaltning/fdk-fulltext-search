from src.search.queries import add_size


def test_should_return_dict_with_size():
    test_dict = {
        "match_all": {}
    }
    result = add_size(test_dict, 5)
    assert 'size' in result


def test_should_return_dict_without_size():
    test_dict = {
        "match_all": {}
    }
    result = add_size(test_dict, None)
    assert 'size' not in result
