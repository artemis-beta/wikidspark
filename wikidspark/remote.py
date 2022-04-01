import datetime
import typing
import pandas
import json
import requests
import urllib.parse

import wikidspark.data_structures as wikid_ds
import wikidspark.wikidata.meta as wikid_meta
import wikidspark.exceptions as wikid_exc


class URLBuilder:
    def __init__(self) -> None:
        self._root_url = f"{wikid_meta.wikidata_urls['site']}/wiki/Special:EntityData"
        self._query_url = urllib.parse.urljoin(wikid_meta.wikidata_urls["query"], "bigdata/namespace/wdq/sparql")

    def fetch_by_id(self, entry_id, revision=None):
        _out = f"{self._root_url}/{entry_id}.json"
        if revision:
            _out += f'?{revision}'
        return(_out)

    def prepare_query(self, query, form='json'):
        return({'url' : self._query_url, 'params' : {'query' : query, 'format' : form}})


class WikidataSPARQLResponse:
    """Response obtained from a WikiData SPARQL Query"""
    def __init__(self, json_response: requests.Response, xml_response: requests.Response) -> None:
        self._json: typing.Any = json_response.json()
        self._xml: typing.Any  = xml_response.text
        self._dataframe: pandas.DataFrame = wikid_ds.as_dataframe(self.json)

    @property
    def json(self) -> typing.Any:
        return self._json

    @property
    def xml(self) -> typing.Any:
        return self._xml

    @property
    def dataframe(self) -> pandas.DataFrame:
        return self._dataframe


class WikidataIDResponse:
    def __init__(self, item_id: int, result: requests.Response, language: typing.Optional[str] = None) -> None:
        language = language or "english"
        language_wikid = wikid_meta.languages[language]
        _result = result.json()['entities'][item_id]


        if language not in wikid_meta.languages:
            raise wikid_exc.LanguageError(language)

        self.__name: str = _result["labels"][language_wikid]["value"]
        self.__id: int = item_id
        self.__language: str = language
        self.__modified = datetime.datetime.strptime(_result["modified"], "%Y-%m-%dT%H:%M:%SZ")
        self.__title = _result['title']
        self.__description = _result['descriptions'][language_wikid]['value']
        self.__aliases = [i["value"] for i in _result["aliases"][language_wikid]]
        self.__site_links = _result['sitelinks']

    @property
    def language(self) -> str:
        return self.__language

    @property
    def modified(self) -> datetime.datetime:
        return self.__modified

    @property
    def title(self) -> typing.List[str]:
        return self.__title

    @property
    def descriptions(self) -> typing.List[str]:
        return self.__description

    @property
    def aliases(self) -> typing.List[str]:
        return self.__aliases

    @property
    def site_links(self) -> typing.List[str]:
        return self.__site_links

    @property
    def name(self) -> typing.List[str]:
        return self.__name

    def __str__(self) -> str:
        return f"WikidataIDResponse({self.__title} ID=Q{self.__id}, lang={self.__language})"

    def __len__(self) -> int:
        return len(self._titles)

