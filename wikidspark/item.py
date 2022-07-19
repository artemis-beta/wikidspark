import abc
import dataclasses


@dataclasses.dataclass
class IDResponseItem(abc.ABC):
    pass


@dataclasses.dataclass
class KeysIDResponseItem(IDResponseItem):
    label: str
    description: str
    alias: str
    sitelink: str
