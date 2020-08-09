from wikidspark.remote import url_builder
from wikidspark.sparql import SPARQL
from wikidspark.data_structures import as_dataframe
import wikidspark.exceptions
from pandas import DataFrame
from wikidspark.wikidata.meta import columns, wikidata_urls, languages
from wikidspark.wikidata.catalogue import *
from wikipedia import search, page

import requests
import json

class query_builder(object):
    def __init__(self, language="english"):
        self._item_var = "item"
        self._query = SPARQL(self._item_var, languages[language].replace(' ','_').lower())
        self._query.SELECT(self._item_var)
        self._property_func_df = self._set_member_functions()
        self._set_columns()

    def _set_member_functions(self):
        _replace_str = {' ': '_', '-': '_', '"': '', '\'' : ''}
        _df_dict = {'function' : [], 'WikiData Property ID' : []}
        for k, v in catalogue.properties.items():
            f_name = v
            for c, n in _replace_str.items():
                f_name = f_name.replace(c,n)
            _df_dict['function'].append(f_name)
            _df_dict['WikiData Property ID'].append(k)
            def func(value):
                if isinstance(value, str):
                    value = find_id(value)
                self._query.WHERE(**{k : value})
            setattr(self, f_name, func)
        return(DataFrame(_df_dict))

    def list_properties(self):
        return(self._property_func_df)

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
            return(as_dataframe(_json_res))
        else:
            _result = requests.get(**_builder.prepare_query(self._query.Build(), form))
            return(getattr(_result, form)())

    def __str__(self):
        return(self._query.Build())

def get_by_id(item_id : str, language=None, keys=None):
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
    return(_result)

def find_id(search_str, get_first=True, language="english"):
    _lang = languages[language]
    _wiki_pages = search(search_str)
    _results = []
    for page in _wiki_pages:
        if ' ' in search_str and not any(i in page for i in search_str.split(' ')):
            continue
        _page_str = page.replace(' ', '_')
        _url = f'https://{_lang}.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={_page_str}&format=json'
        _result = requests.get(_url).json()['query']
        _page0  = list(_result['pages'].keys())[0]
        _id     = _result['pages'][_page0]['pageprops']['wikibase_item']
        if page.lower() == search_str.lower() and get_first:
            return(_id)
        _results.append((page, _id))
    if not _results:
        raise wikidspark.exceptions.IDMatchError(search_str)
    if get_first:
        return(_results[0][1])
    return(_results)

def get_by_name(name : str, language=None, keys=None):
    return(get_by_id(find_id(name), language, keys))

if __name__ in "__main__":
    x = query_builder()
    print(x.list_properties())
