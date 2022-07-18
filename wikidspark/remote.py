import datetime
import logging
import typing
import pandas
import json
import requests
import urllib.parse

import wikidspark.data_structures as wikid_ds
import wikidspark.wikidata.meta as wikid_meta
import wikidspark.exceptions as wikid_exc
import wikidspark.wikidata.common as wikid_com


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
    _logger = logging.getLogger("WikidSpark.WikidataIDResponse")
    def __init__(self, search_id: int, result: requests.Response, language: typing.Optional[str] = None) -> None:
        language = language or "english"

        if language in wikid_meta.languages.values():
            language_wikid = language
        else:
            language_wikid = wikid_meta.languages[language]

        try:
            _res_json = result.json()
        except json.JSONDecodeError as e:
            raise wikid_exc.IDNotFoundError(search_id) from e

        _result = _res_json['entities'][search_id]

        if language not in wikid_meta.languages:
            raise wikid_exc.LanguageError(language)

        try:
            _labels = _result["labels"]
            self.__name = _labels[language_wikid]["value"]
        except KeyError:
            self._logger.warning(f"Could not retrieve name for '{search_id}' for language '{language}'")
            self.__name = None

        self.__id: str = search_id
        self.__language: str = language
        self.__modified = datetime.datetime.strptime(_result["modified"], "%Y-%m-%dT%H:%M:%SZ")
        self.__title = _result['title']

        try:
            _descriptions = _result["descriptions"]
            self.__description = _descriptions[language_wikid]['value']
        except KeyError:
            self._logger.warning(f"Could not retrieve description for '{search_id}' for language '{language}'")
            self.__description = None

        try:
            _aliases = _result["aliases"]
            self.__aliases = [i["value"] for i in _aliases[language_wikid]]
        except KeyError:
            self._logger.warning(f"Could not retrieve aliases for '{search_id}' for language '{language}'")
            self.__aliases = None

        if wikid_com.is_item(search_id):
            self.__site_links = _result['sitelinks']

    @property
    def id(self) -> str:
        return self.__id

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
    def description(self) -> typing.Optional[typing.List[str]]:
        return self.__description

    @property
    def aliases(self) -> typing.Optional[typing.List[str]]:
        return self.__aliases

    @property
    def site_links(self) -> typing.List[str]:
        return self.__site_links

    @property
    def name(self) -> typing.Optional[typing.List[str]]:
        return self.__name

    def __str__(self) -> str:
        return f"WikidataIDResponse({self.__title} ID=Q{self.__id}, lang={self.__language})"

    def __len__(self) -> int:
        return len(self._titles)

