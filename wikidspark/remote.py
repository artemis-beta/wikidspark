import os

class url_builder(object):
    def __init__(self, domain):
        self._root_url = os.path.join(domain["site"], "wiki", "Special:EntityData")
        self._query_url = os.path.join(domain["query"], "sparql")

    def fetch_by_id(self, entry_id, revision=None):
        _out = f"{os.path.join(self._root_url, entry_id)}.json"
        if revision:
            _out += '?'+str(revision)
        return(_out)

    def prepare_query(self, query, form='json'):
        return({'url' : self._query_url, 'params' : {'query' : query, 'format' : form}})
