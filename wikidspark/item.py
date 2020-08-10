from wikidspark.data_structures import as_dataframe

class QItem(object):
    def __init__(self, json_response, xml_response):
        self.json = json_response.json()
        self.xml  = xml_response.text
        self.dataframe = as_dataframe(self.json)
        self._attach_members()

    def _attach_members(self):
        pass
