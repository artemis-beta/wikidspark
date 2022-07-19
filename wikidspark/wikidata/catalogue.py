import json
import os.path

loc_dir = os.path.dirname(__file__)


class _catalogue:
    def __init__(self) -> None:
        if not os.path.exists(os.path.join(loc_dir, "properties.json")):
            raise FileNotFoundError("Properties file not found.")

        with open(os.path.join(loc_dir, "properties.json")) as f:
            self.properties = json.load(f)

        if os.path.exists(os.path.join(loc_dir, "items.json")):
            with open(os.path.join(loc_dir, "items.json")) as f:
                self._items = json.load(f)
        else:
            self._items = {}


catalogue = _catalogue()
