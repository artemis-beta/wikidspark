from wikidspark.wikidata.meta import prefixes


class SPARQL:
    def __init__(self, item_label="item", language_id="en"):
        self._clear()
        self._selection = [item_label]
        self._n_entries = -1
        self._language = language_id
        self._item = item_label
        self._ordering = None

    def _select_str(self):
        if not self._selection or not isinstance(self._selection, list):
            raise AssertionError("Failed to retrieve SELECT string")
        return "SELECT DISTINCT " + " ".join(f"?{s}" for s in self._selection)

    def _where_str(self):
        return (
            (
                "\t"
                + "\n\t".join(
                    [
                        f'?{self._item} {prefixes["property"]}:{k} '
                        + f'{prefixes["entity"]}:{v} .'
                        for k, v in self._where.items()
                    ]
                )
                + "\n"
            )
            if self._where
            else ""
        )

    def _statement_str(self):
        return (
            (
                "\t"
                + "\n\t".join(
                    [
                        f'?item p:{prop} ?statement0 .\n'
                        + f'?statement0 (ps:{prop}) "{value}" .'
                        for prop, value in self._statements.items()
                    ]
                )
                + "\n"
            )
            if self._statements
            else ""
        )

    def _service_str(self):
        if not self._service:
            return ""
        _out_srv = [
            f'\tSERVICE {s["tag"]}' + " {" + " ".join(s["args"].values()) + "} ."
            for s in self._service
        ]
        return "\n\t".join(_out_srv) + "\n"

    def _limit_str(self):
        return "" if self._n_entries == -1 else f"\nLIMIT {self._n_entries}"

    def _filter_str(self):
        if not self._filter:
            return ""
        _out_filt = [f"\tFILTER {f} ." for f in self._filter]
        return "\n\t".join(_out_filt) + "\n"

    def _order_str(self):
        if not self._ordering:
            return ""
        _order_str = "ORDER BY "
        _order_str += (
            f"DESC(?{self._ordering[0]})"
            if self._ordering[1]
            else f"?{self._ordering[0]}"
        )
        _order_str += "\n"
        return _order_str

    def _clear(self):
        self._where = {}
        self._service = []
        self._filter = []
        self._statements = {}

    def SELECT(self, *args):
        if any("Label" in arg for arg in args):
            self.SERVICE(
                f'{prefixes["ontology"]}:label',
                service_param=f'{prefixes["big-data"]}:serviceParam',
                lang=f'{prefixes["ontology"]}:language "[AUTO_LANGUAGE], {self._language}"',
            )
        self._selection += [*args]

    def ORDER_BY(self, value, desc=False):
        self._ordering = (value, desc)

    def WHERE(self, **kwargs):
        self._where.update(**kwargs)

    def SERVICE(self, service_tag, **kwargs):
        if {"tag": service_tag, "args": kwargs} not in self._service:
            self._service += [{"tag": service_tag, "args": kwargs}]

    def LIMIT(self, n_entries):
        self._n_entries = n_entries

    def FILTER_EXISTS(self, **kwargs):
        for _, v in kwargs.items():
            self._filter.append(
                "EXISTS {?item" + prefixes["property"] + ":" + v + " } ."
            )

    def STATEMENT(self, **kwargs):
        self._statements.update(**kwargs)

    def FILTER_NOT_EXISTS(self, **kwargs):
        for _, v in kwargs.items():
            self._filter.append(
                "NOT EXISTS {?item" + prefixes["property"] + ":" + v + " } ."
            )

    def FILTER_RELATION(self, relation="=", **kwargs):
        for k, v in kwargs.items():
            self._filter.append(f'( {prefixes["property"]}:{k} {relation} "{v}" ) .')

    def build(self) -> str:
        _query_str = self._select_str()
        _query_str += """
WHERE
{
"""
        _query_str += self._where_str()
        _query_str += self._statement_str()
        _query_str += self._service_str()
        _query_str += self._filter_str()
        _query_str += """
}"""
        _query_str += self._order_str()
        _query_str += self._limit_str()
        return _query_str
