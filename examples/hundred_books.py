#########################################################
#                                                       #
#   Find the first hundred books in the Database        #
#                                                       #
#########################################################
from wikidspark.query import query_builder
my_query = query_builder("english")

my_query.instance_of('book')   # P31 = Q571
my_query.Description = True
my_query.Label = True

# Fetch maximum of 100 results and print DataFrame output
result = my_query.get(limit=100)
print(result.dataframe)
