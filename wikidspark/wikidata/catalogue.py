import json
from os.path import exists, join, realpath, basename

loc_dir = realpath(__file__).replace(basename(__file__), '')

class _catalogue(object):
    def __init__(self):
        assert exists(join(loc_dir, 'properties.json')), "Properties file not found."
        self.properties = json.load(open(join(loc_dir, 'properties.json')))

        if exists(join(loc_dir, 'items.json')):
            self._items = json.load(loc_dir, 'items.json')
        else:
            self._items = {}

catalogue = _catalogue()

