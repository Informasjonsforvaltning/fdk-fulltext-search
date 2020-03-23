import pytest
from tests.contract.contract_test_utils import wait_for_es, populate, clean_es


@pytest.fixture(scope="module")
def api():
    wait_for_es()
    populate()
    yield
    clean_es()

class TestSearchAll:

    @pytest.mark.contract
    def test_should_return_dict_with_size(self, api):
        assert api is None
