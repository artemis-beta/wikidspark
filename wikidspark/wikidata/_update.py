import json
import os.path

import click
import html_to_json
import requests
import tqdm

loc_dir = os.path.dirname(__file__)


@click.command("update-properties")
def _update_properties() -> None:
    _webpage_dat: str = requests.get(
        "https://www.wikidata.org/wiki/Wikidata:Database_reports/List_of_properties/all"
    ).text
    _tab_cut: str = _webpage_dat.split('<table class="wikitable sortable">')[-1]
    _tab_cut = '<table class="wikitable sortable">\n' + _tab_cut
    _tab_cut = _tab_cut.split("</table>")[0] + "</table>"
    _json_dat = html_to_json.convert(_tab_cut)
    _tab_dat = _json_dat["table"][0]["tbody"][0]["tr"]
    _properties = {
        prop["td"][0]["a"][0]["_value"]: prop["td"][1]["_value"]
        for prop in tqdm.tqdm(_tab_dat[1:])
    }

    with open(os.path.join(loc_dir, "properties.json"), "w", encoding="utf-8") as f:
        json.dump(_properties, f, indent=2)


if __name__ in "__main__":
    _update_properties()
