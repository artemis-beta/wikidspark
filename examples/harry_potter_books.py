
#########################################################
#                                                       #
#   Build a Query Searching for Harry Potter Books      #
#                                                       #
#########################################################
from wikidspark.query import query_builder

query = query_builder()
query.Label = True
query.Description = False
query.author('JK Rowling')               # P50 = Q34660
query.part_of_the_series('Harry Potter') # P179 = Q8337
result = query.get(10, 'df')
print(result)
