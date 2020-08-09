from wikidspark.query import get_by_id
import wikidspark.exceptions
import time # Must not overload server
from tqdm import tqdm
import json
from os.path import exists, join, realpath, basename

loc_dir = realpath(__file__).replace(basename(__file__), '')

def _update_properties(x_l, x_u):
    assert x_l > 16, "Lowest property is P17"
    if exists(join(loc_dir, 'properties.json')):
        _properties = json.load(open(join(loc_dir, 'properties.json')))
    else:
        _properties = {}
    for i in tqdm(range(x_l, x_u), desc='Fetching Properties'):
        if 'P{i}' in _properties:
            continue
        try:
            result = get_by_id(f'P{i}')
        except wikidspark.exceptions.IDNotFoundError:
            continue
        _properties[f'P{i}'] = result['labels']['en']['value']
        time.sleep(2)
    json.dump(_properties, open(join(loc_dir, 'properties.json'), 'w'))


if __name__ in "__main__":
    _update_properties(49, 52)

