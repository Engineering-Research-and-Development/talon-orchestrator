import json
from api.utils.RestResponse import RestResponse 

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, RestResponse):
            return obj.__dict__
        return super().default(obj)