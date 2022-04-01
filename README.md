# WikidSpark
![WikidSpark](https://github.com/artemis-beta/wikidspark/workflows/WikidSpark/badge.svg)[![codecov](https://codecov.io/gh/artemis-beta/wikidspark/branch/master/graph/badge.svg)](https://codecov.io/gh/artemis-beta/wikidspark)[![CodeFactor](https://www.codefactor.io/repository/github/artemis-beta/wikidspark/badge)](https://www.codefactor.io/repository/github/artemis-beta/wikidspark)[![GitHub](https://img.shields.io/github/license/artemis-beta/wikidspark)](https://github.com/artemis-beta/wikidspark/blob/master/LICENSE)

WikidSpark is a python module with the aim of providing easy access to the WikiData SPARQL database. The aim is to provide a friendly method which allows those unfamiliar with SPARQL and databases in general to still access the information.

## Querying WikiData
There are currently two methods for retrieving data from the WikiData site.

### Direct Query
The first is query the site directly by passing the relevant id (`QXYZ`) to the query service. Two methods can be used to do this: `get_by_id` or `get_by_name`. Both of these methods come with two optional arguments for filtering the results:

```Python
from wikidspark.query import get_by_id

# Search for the Douglas Adams WikiData entry
dga_id = 'Q42'

dga_query_full = get_by_id(dga_id)
dga_query_language = get_by_id(dga_id, language='french')
```
the retrieve-by-name method currently makes use of the pre-requisite `wikipedia` model to find items relevant to the search, making it limited in terms of only displaying those entries which have an article attached to them. The function returns the first match it finds:
```Python
from wikidspark.query import get_by_name

dga_query_full = get_by_name('Douglas Adams')
dga_query_filtered = get_by_name('Douglas Adams', language='english', keys=['labels', 'descriptions'])
```
for a wider search it is recommended to use the `find_item` function to firstly return the relevant id, then use the `get_by_id` function. The `find_item` function has additional arguments to fetch only the first result (the default) or a list of matches, and to specify the wikipedia language:

```Python
dga_id = find_id('Douglas Adams')
london_ids = find_id('London', get_first=False, language='english')
```

### Built Query
This method uses a class `QueryBuilder` to construct a SPARQL query to be sent to the WikiData query service. The query is built in stages, firstly by defining an instance of the builder (with the optional argument `language`),then adding conditions before finally fetching the results as a `QItem` object. This object allows you to view the data as XML, JSON or a Pandas Dataframe. The data returned currently has the additional properties `Label`, `Description` and `AltLabel` which are turned off by default but can be activated.

```Python
# Find first 100 books
from wikidspark.query import QueryBuilder
my_query = QueryBuilder("english")

my_query.instance_of('book')
my_query.Description = True
my_query.Label = True

result = my_query.get(limit=100)
json_res = result.json
xml_res  = result.xml
df_res   = result.dataframe
```

The functions available to the `QueryBuilder` class (e.g. `instance_of`) are based on an extensive list of WikiData properties, the full list can be fetched as a dataframe:

```Python
QueryBuilder().list_properties()
```
