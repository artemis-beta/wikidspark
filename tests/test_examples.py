import pytest
import pathlib
import os

import wikidspark.examples.harry_potter_books as wiki_ex_hp
import wikidspark.examples.hundred_books as wiki_ex_100
import wikidspark.examples.uk_railway_stations as wiki_ex_ukstat
import wikidspark.examples.crs as wiki_crs


EXAMPLE_DIR = os.path.join(pathlib.Path(__file__).parents[1], "examples")


@pytest.mark.examples
def test_harry_potter_query() -> None:
    assert len(wiki_ex_hp.harry_potter_books().dataframe) == 10


@pytest.mark.examples
def test_hundred_books_query() -> None:
    assert len(wiki_ex_100.hundred_books().dataframe) == 100


@pytest.mark.examples
def test_uk_railway_station_query() -> None:
    assert len(wiki_ex_ukstat.uk_railway_stations().dataframe) == 100


@pytest.mark.examples
def test_crs_query() -> None:
    assert wiki_crs.crs_search().dataframe.iloc[0]["Label"] == "Richmond station"
