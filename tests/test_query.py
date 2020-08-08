import wikidspark.exceptions
import pytest
from wikidspark.query import *

class TestQuerySystem(object):
    def test_id_retrieval_success(self):
        test_search = 'Douglas Adams'
        assert find_id(test_search) == 'Q42'

    def test_id_retrieval_failure(self):
        test_search = 'Intyna'
        with pytest.raises(wikidspark.exceptions.IDMatchError):
            find_id(test_search)

    def test_invalid_property(self):
        query = query_builder()
        with pytest.raises(wikidspark.exceptions.PropertyNotFoundError):
            query.order_by('foobar')

    def test_id_search_success(self):
        test_id = 'Q42'
        assert len(get_by_id(test_id)) > 0

    def test_id_search_failure(self):
        test_id = 'Q999999999999999999'
        with pytest.raises(wikidspark.exceptions.IDNotFoundError):
            get_by_id(test_id)
