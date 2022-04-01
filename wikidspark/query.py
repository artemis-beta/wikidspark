import typing
from wikidspark.remote import URLBuilder, WikidataIDResponse, WikidataSPARQLResponse
from wikidspark.sparql import SPARQL
import wikidspark.wikidata.meta as wikid_meta
import wikidspark.wikidata.common as wikid_com
from wikidspark.wikidata.catalogue import *
import wikidspark.exceptions

import requests
import time
import json

from pandas import DataFrame
from wikipedia import search

class QueryBuilder:
    def __init__(self, language: str = "english") -> None:
        self._item_var = "item"
        self._lang = language
        self._query = SPARQL(self._item_var, wikid_meta.languages[self._lang.replace(' ', '_').lower()])
        self._set_columns()
        self._property_func_df = self._create_member_functions()

    def _create_member_functions(self) -> None:
        _replace_str = {' ': '_', '-': '_', '"': '', '\'' : ''}
        _df_dict = {'function' : [], 'WikiData Property ID' : []}
        for k, v in catalogue.properties.items():
            f_name = f'{v}'
            for c, n in _replace_str.items():
                f_name = f_name.replace(c,n)
            _df_dict['function'].append(f_name)
            _df_dict['WikiData Property ID'].append(k)
            setattr(self, f_name, _member_factory_func(self._query, k))
        return DataFrame(_df_dict)

    def list_properties(self):
        return self._property_func_df

    def _set_columns(self):
        for group in wikid_meta.columns:
            for member in wikid_meta.columns[group]:
                setattr(self, member, False)

    def has(self, key):
        self._query.FILTER_EXISTS(key)

    def order_by(self, value=None):
        if not hasattr(self, value):
            raise wikidspark.exceptions.PropertyNotFoundError(value)
        self._query.SELECT(self._item_var+value)

    def get(self, limit=None):
        if limit:
            self._query.LIMIT(limit)
        for group in wikid_meta.columns:
            for member in wikid_meta.columns[group]:
                if getattr(self, member):
                    self._query.SELECT(self._item_var+member)

        _builder = URLBuilder()
        _json_query: str = _builder.prepare_query(self._query.Build(), 'json')

        _result_json: requests.Response = requests.get(**_json_query)

        if _result_json.status_code != 200:
            raise wikidspark.exceptions.ConnectionError(_result_json)

        time.sleep(1)
        _result_xml  = requests.get(**_builder.prepare_query(self._query.Build(), 'xml'))

        if _result_xml.status_code != 200:
            raise wikidspark.exceptions.ConnectionError(_result_xml)

        return WikidataSPARQLResponse(_result_json, _result_xml)

    def __str__(self):
        return self._query.Build()


def get_by_id(item_id: int, language: typing.Optional[str] = None) -> WikidataIDResponse:
    if not wikid_com.check_id(item_id):
        raise AssertionError("Invalid Item ID")

    language = language or "english"

    try:
        _url = URLBuilder().fetch_by_id(item_id)
        _result = requests.get(_url)
    except json.decoder.JSONDecodeError as e:
        raise wikidspark.exceptions.IDNotFoundError(item_id) from e

    return WikidataIDResponse(item_id, _result, language)


def find_id(search_str: str, get_first: bool = True, language: str = "english") -> str:
    _wiki_pages = search(search_str)
    if not _wiki_pages:
        raise wikidspark.exceptions.IDMatchError(search_str)
    _url = 'https://{}.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={}&format=json'

    def _id_from_result(wiki_str: str) -> typing.Tuple[str, str]:
        _result = requests.get(_url.format(wikid_meta.languages[language], wiki_str))
        _page0 = list(_result.json()['query']['pages'].keys())[0]
        return _result.json()['query']['pages'][_page0]['pageprops']['wikibase_item']

    if search_str.lower() in [i.lower() for i in _wiki_pages]:
        _id = _id_from_result(search_str.replace(' ', '_'))
        return _id

    elif get_first:
        _id = _id_from_result(_wiki_pages[0])
        return _id

    _results = []
    for page in _wiki_pages:
        if ' ' in search_str and not any(i in page for i in search_str.split(' ')):
            continue
        _page_str = page.replace(' ', '_')
        _id = _id_from_result(_page_str)
        _results.append((page, _id))
    if not _results:
        raise wikidspark.exceptions.IDMatchError(search_str)
    return _results


def get_by_name(name: str, language: typing.Optional[str] = None) -> typing.Dict[str, WikidataIDResponse]:
    return get_by_id(find_id(name), language)


def _member_factory_func(query: SPARQL, identifier: str) -> typing.Callable:
    def func(value):
        value = value if wikid_com.check_id(value) else find_id(value)
        query.WHERE(**{identifier : value})
    return func
