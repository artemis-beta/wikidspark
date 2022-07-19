#########################################################
#                                                       #
#   Build a Query Searching for Harry Potter Books      #
#                                                       #
#########################################################
from wikidspark.query import QueryBuilder
from wikidspark.remote import WikidataSPARQLResponse


def harry_potter_books() -> WikidataSPARQLResponse:
    query = QueryBuilder()
    query.Label = True
    query.AltLabel = False
    query.Description = False
    query.author("JK Rowling")  # P50 = Q34660
    query.part_of_the_series("Harry Potter")  # P179 = Q8337
    return query.get()


if __name__ in "__main__":
    print(harry_potter_books().dataframe)
