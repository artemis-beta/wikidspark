import abc
import typing
import pandas
import requests
import dataclasses

import wikidspark.data_structures as wikid_ds


@dataclasses.dataclass
class IDResponseItem(abc.ABC):
    pass

@dataclasses.dataclass
class KeysIDResponseItem(IDResponseItem):
    label: str
    description: str
    alias: str
    sitelink: str