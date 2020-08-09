from wikidspark.remote import url_builder
from wikidspark.sparql import SPARQL
from wikidspark.data_structures import as_dataframe
from wikidspark.wikidata.meta import columns, wikidata_urls, languages
from wikidspark.wikidata.catalogue import *
import wikidspark.exceptions

import re
import requests
import json

from pandas import DataFrame
from wikipedia import search, page

class query_builder(object):
    def __init__(self, language="english"):
        self._item_var = "item"
        self._lang = language
        self._query = SPARQL(self._item_var, languages[self._lang.replace(' ', '_').lower()])
        self._set_columns()
        self._property_func_df = self._create_member_functions()
    
    def _create_member_functions(self):
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
        for group in columns:
            for member in columns[group]:
                setattr(self, member, False)

    def has(self, key):
        self._query.FILTER_EXISTS(key)

    def order_by(self, value=None):
        if not hasattr(self, value):
            raise wikidspark.exceptions.PropertyNotFoundError(value)
        self._query.SELECT(self._item_var+value)

    def get(self, n_entries=10, form='json'):
        self._query.LIMIT(n_entries)
        for group in columns:
            for member in columns[group]:
                if getattr(self, member):
                    self._query.SELECT(self._item_var+member)
        _builder = url_builder(wikidata_urls)
        if form == 'df':
            _result = requests.get(**_builder.prepare_query(self._query.Build(), 'json'))
            _json_res = _result.json()
            return as_dataframe(_json_res)
        else:
            _result = requests.get(**_builder.prepare_query(self._query.Build(), form))
            return getattr(_result, form)()

    def __str__(self):
        return self._query.Build()

def check_id(item_id):
    return len(re.findall(r'Q\d+', item_id)) > 0

def get_by_id(item_id : str, language=None, keys=None):
    assert check_id(item_id), "Invalid Item ID"
    try:
        _result = requests.get(url_builder(wikidata_urls).fetch_by_id(item_id)).json()['entities'][item_id]
    except json.decoder.JSONDecodeError:
        raise wikidspark.exceptions.IDNotFoundError(item_id)
    if language:
        _result['labels'] = _result['labels'][languages[language]]['value']
        _result['descriptions'] = _result['descriptions'][languages[language]]['value']
        _result['aliases'] = [i['value'] for i in _result['aliases'][languages[language]]]
        _result['sitelinks'] = _result['sitelinks'][f'{languages[language]}wiki']
    if keys:
        _result = {k:_result[k] for k in keys if k in _result}
    return _result

def find_id(search_str, get_first=True, language="english"):
    _lang = languages[language.replace(' ', '_').lower()]
    _wiki_pages = search(search_str)
    if not _wiki_pages:
        raise wikidspark.exceptions.IDMatchError(search_str)
    _url = 'https://{}.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={}&format=json'

    def _id_from_result(wiki_str):
        _result = requests.get(_url.format(languages[language], wiki_str))
        _page0 = list(_result.json()['query']['pages'].keys())[0]
        _id    = _result.json()['query']['pages'][_page0]['pageprops']['wikibase_item']
        return _id

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
    if get_first:
        return _results[0][1]
    return _results

def get_by_name(name : str, language=None, keys=None):
    return get_by_id(find_id(name), language, keys)

def _member_factory_func(query, identifier):
    def func(value):
        value = value if check_id(value) else find_id(value)
        query.WHERE(**{identifier : value})
    return func
