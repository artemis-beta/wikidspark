#########################################################
#                                                       #
#   Build a Query Searching for UK Stations by CRS Code #
#                                                       #
#########################################################
from wikidspark.query import QueryBuilder
from wikidspark.remote import WikidataSPARQLResponse

def crs_search() -> WikidataSPARQLResponse:
    RICHMOND_LONDON = "RMD"
    query = QueryBuilder()
    query.Label = True
    query.AltLabel = False
    query.Description = False
    query.property_equals("P4755", RICHMOND_LONDON)
    return query.get()


if __name__ in "__main__":
    print(crs_search().dataframe)
