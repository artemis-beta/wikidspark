import typing


import wikidspark.wikidata.meta as wkd_meta


class SPARQL:
    def __init__(self, language: str = "en", limit: int=100) -> None:
        self._distinct: bool = False
        self.language: str = language
        self.limit: int = limit
        self._where: typing.Dict[str, str] = {}
        self._select_labels: typing.Dict[str, bool] = {}
        self._group_by: typing.List[str] = []
        self._order_by: typing.List[str] = []

    @property
    def DISTINCT(self) -> "SPARQL":
        self._distinct = True
        return self

    def _select_variable(self, property: str) -> str:
        return f"?var{property}"

    def WHERE(self, property: str, value: typing.Optional[str]=None, show: bool=True, label: bool=True) -> "SPARQL":
        value = value or self._select_variable(property)
        self._where[property] = value
        if show:
            self._select_labels[property] = label
        return self

    def GROUP_BY(self, property: str) -> "SPARQL":
        self._group_by.append(property)
        return self

    def ORDER_BY(self, property: str) -> "SPARQL":
        self._order_by.append(property)
        return self

    @property
    def where_str(self) -> str:
        if not self._where:
            return ""
        _out_str: str = "WHERE {"
        _out_str += f"\n\t{self.service_str}\n\t"
        _statements: typing.List[str] = [
            f"{self._select_variable(k)} "
            f"{wkd_meta.prefixes['property']}:{k} "
            f"{wkd_meta.prefixes['entity']}:{v}."
            for k, v in self._where.items()
        ]
        _out_str += "\n\t".join(_statements)
        _out_str += "\n}"
        
        return _out_str

    @property
    def order_by_str(self) -> str:
        return "ORDER BY " + " ".join(f"ASC(UCASE({self._select_variable(k)}Label))" for k in self._order_by)

    @property
    def service_str(self) -> str:
        return 'SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],'+self.language+'". }'

    @property
    def group_by_str(self) -> str:
        return "\n".join(f"GROUP BY {self._select_variable(i)}Label" for i in self._group_by)

    @property
    def limit_str(self) -> str:
        return f"LIMIT {self.limit}"

    @property
    def selection_str(self) -> str:
        _select_str: str = "SELECT "
        if self._distinct:
            _select_str += "DISTINCT "
        _select_str += "\n"
        
        for selection, show_label in self._select_labels.items():
            if selection not in self._group_by:
                _select_str += "\t"+self._select_variable(selection)
            else:
                _select_str += "\t"
            if show_label:
                _select_str += " "+self._select_variable(selection)+"Label"
            _select_str += "\n"

        return _select_str

    def build(self) -> str:
        _query_str = self.selection_str
        _query_str += f"\n{self.where_str}"
        _query_str += f"\n{self.group_by_str}" if self.group_by_str else ""
        _query_str += f"\n{self.order_by_str}" if self.order_by_str else ""
        _query_str += f"\n{self.limit_str}"
        return _query_str
