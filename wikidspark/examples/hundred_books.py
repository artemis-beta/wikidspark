#########################################################
#                                                       #
#   Find the first hundred books in the Database        #
#                                                       #
#########################################################
from wikidspark.query import QueryBuilder
from wikidspark.remote import WikidataSPARQLResponse


def hundred_books() -> WikidataSPARQLResponse:
    my_query = QueryBuilder("english")

    my_query.instance_of('book')   # P31 = Q571
    my_query.Description = True
    my_query.Label = True

    # Fetch maximum of 100 results and print DataFrame output
    return my_query.get(limit=100)


if __name__ in "__main__":
    print(hundred_books().dataframe)
