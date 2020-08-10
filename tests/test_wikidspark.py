from wikidspark import __version__
import wikidspark.exceptions
import pytest
from wikidspark.query import query_builder, _member_factory_func, get_by_id, get_by_name, find_id
import pprint
import copy

def test_version():
    assert __version__ == '0.1.0'

query = query_builder()
query.Label = True
query.AltLabel = True
query.Description = True
query.instance_of('locomotive')
result = query.get(limit=50)

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
        assert len(result.json['results']['bindings']) == 50

    def test_query_keys(self):
        assert any(all(a in list(result.json['results']['bindings'][i].keys()) for a in ['itemLabel', 'itemDescription', 'itemAltLabel']) for i in range(50)) 

    def test_dataframe(self):
        assert len(result.dataframe) == 50

    def test_member_function_build(self):
        _query = query_builder()
        _member_factory_func(_query._query, 'P31')('Q2345')
        assert _query._query._where['P31'] == 'Q2345'
