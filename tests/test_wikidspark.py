import wikidspark.exceptions
import pytest
from wikidspark.query import QueryBuilder, _member_factory_func, get_by_id, find_id
from wikidspark.remote import WikidataSPARQLResponse


@pytest.fixture
def query_builder() -> QueryBuilder:
    query = QueryBuilder()
    query.Label = True
    query.AltLabel = True
    query.Description = True
    query.instance_of("locomotive")
    return query


@pytest.fixture
def query_response(query_builder: QueryBuilder) -> WikidataSPARQLResponse:
    return query_builder.get(50)


def test_id_retrieval_success():
    test_search = "Douglas Adams"
    _item_result = find_id(test_search)
    assert _item_result == "Q42"


def test_id_retrieval_failure():
    test_search = "Intyna"
    with pytest.raises(wikidspark.exceptions.IDMatchError):
        find_id(test_search)


def test_invalid_property(query_builder: QueryBuilder):
    with pytest.raises(wikidspark.exceptions.PropertyNotFoundError):
        query_builder.order_by("foobar")


def test_id_search_success():
    test_id = "Q42"
    assert get_by_id(test_id).name == "Douglas Adams"


def test_id_search_failure():
    test_id = "Q999999999999999999"
    with pytest.raises(wikidspark.exceptions.IDNotFoundError):
        get_by_id(test_id)


def test_query_length(query_response: WikidataSPARQLResponse):
    assert len(query_response.json["results"]["bindings"]) == 50


def test_query_keys(query_response: WikidataSPARQLResponse):
    assert any(
        all(
            a in list(query_response.json["results"]["bindings"][i].keys())
            for a in ["itemLabel", "itemDescription", "itemAltLabel"]
        )
        for i in range(50)
    )


def test_dataframe(query_response: WikidataSPARQLResponse):
    assert len(query_response.dataframe) == 50


def test_member_function_build():
    _query = QueryBuilder()
    _member_factory_func(_query._query, "P31")("Q2345")
    assert _query._query._where["P31"] == "Q2345"
