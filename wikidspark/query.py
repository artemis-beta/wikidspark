from wikidspark.remote import url_builder
from wikidspark.sparql import SPARQL
from wikidspark.data_structures import as_dataframe
import wikidspark.exceptions
from wikidspark.wikidata.properties import properties, wikidata_urls, languages
from wikipedia import search, page

import requests
import json

class query_builder(object):
    def __init__(self, language="english"):
        self._item_var = "item"
        self._query = SPARQL(self._item_var, languages[language].replace(' ','_').lower())
        self._query.SELECT(self._item_var)
        self._set_properties()

    def _set_properties(self):
        for prop in properties:
            for member in properties[prop]:
                setattr(self, member, False)

    def has(self, key):
        self._query.FILTER_EXISTS(key)

    def is_instance(self, value):
        if isinstance(value, str):
            value = find_id(value)
        self._query.WHERE(P31 = value)

    def order_by(self, value=None):
        if not hasattr(self, value):
            raise wikidspark.exceptions.PropertyNotFoundError(value)
        self._query.SELECT(self._item_var+value)

    def get(self, n_entries=10, form='json'):
        self._query.LIMIT(n_entries)
        for prop in properties:
            for member in properties[prop]:
                if getattr(self, member):
                    self._query.SELECT(self._item_var+member)
        _builder = url_builder(wikidata_urls)
        if form == 'df':
            _result = getattr(requests.get(**_builder.prepare_query(self._query.Build(), 'json')), 'json')()
            return(as_dataframe(_result))
        else:
            _result = getattr(requests.get(**_builder.prepare_query(self._query.Build(), form)), form)()
            return(_result)

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
    x.is_instance('film')
    x.Label = True
    x.Description = True
    print(x.get(10, 'df'))
