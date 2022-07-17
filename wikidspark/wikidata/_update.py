import wikidspark.query as wikid_query
import wikidspark.exceptions
import time # Must not overload server
from tqdm import tqdm
import click
import json
import os.path


loc_dir = os.path.dirname(__file__)

@click.command("update-properties")
@click.argument("range_lower", type=click.INT)
@click.argument("range_upper", type=click.INT)
def _update_properties(range_lower: int, range_upper: int) -> None:
    assert range_lower > 16, "Lowest property is P17"
    if os.path.isfile(os.path.join(loc_dir, 'properties.json')):
        _properties = json.load(open(os.path.join(loc_dir, 'properties.json')))
    else:
        _properties = {}
    for i in tqdm(range(range_lower, range_upper), desc='Fetching Properties'):
        if f'P{i}' in _properties:
            continue
        try:
            result = wikid_query.get_by_id(f'P{i}')
        except wikidspark.exceptions.IDNotFoundError:
            continue
        _properties[f'P{i}'] = result.name
        time.sleep(2)
    json.dump(_properties, open(os.path.join(loc_dir, 'properties.json'), 'w'), indent=2)


if __name__ in "__main__":
    _update_properties()

