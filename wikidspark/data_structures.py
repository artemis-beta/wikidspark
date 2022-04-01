import pandas as pd

def as_dataframe(query_result : str) -> pd.DataFrame:
    """Converts the given query result string to a Pandas Dataframe"""
    _df_dict = {'id': []}
    cols = query_result['head']['vars']
    for col in cols:
        if col == 'item':
            _df_dict['url'] = []
        else:
            _df_dict[col.replace('item', '')] = []
    results = query_result['results']['bindings']
    for result in results:
        _df_dict['id'].append(result['item']['value'].split('entity/')[1])
        for col in cols:
            try:
                if col == 'item':
                    _df_dict['url'].append(result[col]['value'])
                    continue
                _df_dict[col.replace('item','')].append(result[col]['value'])
            except KeyError:
                _df_dict[col.replace('item','')].append('')

    return(pd.DataFrame(_df_dict))

