import pandas as pd

class DataFrame(pd.DataFrame):
    def from_query(self, query : str):
        pass

    def from_json(self, query_result : str):
        pass
