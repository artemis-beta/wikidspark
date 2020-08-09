from wikidspark import __version__
import wikidspark.exceptions
import pytest
from wikidspark.query import query_builder, _member_factory_func, get_by_id, get_by_name, find_id
import pprint
import time
import copy

def test_version():
    assert __version__ == '0.1.0'

query = query_builder()
query.Label = True
query.AltLabel = True
query.Description = True
query.instance_of('locomotive')
query_df = copy.deepcopy(query)
built_query_result = query.get(100)
time.sleep(5) # So as to not send two queries at same time
built_query_df = query_df.get(10, 'df')

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

    def test_pandas_df(self):
        assert len(built_query_df) == 10

    def test_member_function_build(self):
        _query = query_builder()
        _member_factory_func(_query._query, 'P31')('Q2345')
        assert _query._query._where['P31'] == 'Q2345'
