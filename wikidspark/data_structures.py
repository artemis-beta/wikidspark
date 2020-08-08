import pandas as pd

def as_dataframe(query_result : str):
    _df_dict = {}
    _df_dict['id'] = []
    cols = query_result['head']['vars']
    for col in cols:
        _df_dict[col.replace('item', '')] = []
    results = query_result['results']['bindings']
    for result in results:
        _df_dict['id'].append(result['item']['value'].split('entity/')[1])
        for col in cols:
            try:
                _df_dict[col.replace('item','')].append(result[col]['value'])
            except KeyError:
                _df_dict[col.replace('item','')].append('')

    return(pd.DataFrame(_df_dict))

