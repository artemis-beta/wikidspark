#########################################################
#                                                       #
#           Return 100 UK railway stations              #
#                                                       #
#########################################################
from wikidspark.query import QueryBuilder
from wikidspark.remote import WikidataSPARQLResponse


def uk_railway_stations() -> WikidataSPARQLResponse:
    query = QueryBuilder()
    query.instance_of("train station")
    query.country("United Kingdom")
    query.Label = True
    return query.get(100)


if __name__ in "__main__":
    print(uk_railway_stations().dataframe)
