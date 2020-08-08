from wikidspark import __version__
import wikidspark.exceptions
import pytest
from wikidspark.query import *
import pprint

def test_version():
    assert __version__ == '0.1.0'

query = query_builder()
query.Label = True
query.AltLabel = True
query.Description = True
query.is_instance('locomotive')
built_query_result = query.get(100)

class TestQuerySystem(object):
    def test_id_retrieval_success(self):
        test_search = 'Douglas Adams'
        assert find_id(test_search) == 'Q42'

    def test_id_retrieval_failure(self):
        test_search = 'Intyna'
        with pytest.raises(wikidspark.exceptions.IDMatchError):
            find_id(test_search)

    def test_invalid_property(self):
        with pytest.raises(wikidspark.exceptions.PropertyNotFoundError):
            query.order_by('foobar')

    def test_id_search_success(self):
        test_id = 'Q42'
        assert len(get_by_id(test_id)) > 0

    def test_id_search_failure(self):
        test_id = 'Q999999999999999999'
        with pytest.raises(wikidspark.exceptions.IDNotFoundError):
            get_by_id(test_id)

    def test_query_length(self):
        assert len(built_query_result['results']['bindings']) == 100

    def test_query_keys(self):
        assert all(a in built_query_result['results']['bindings'][42].keys() for a in ['itemLabel', 'itemDescription', 'itemAltLabel']) 
