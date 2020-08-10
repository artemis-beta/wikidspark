
#########################################################
#                                                       #
#           Return 100 UK railway stations              #
#                                                       #
#########################################################
from wikidspark.query import query_builder

query = query_builder()
query.instance_of('train station')
query.country('United Kingdom')
query.Label = True
result = query.get(100)
print(result.dataframe)
