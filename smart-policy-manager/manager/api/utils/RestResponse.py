import json
from flask import jsonify

class RestResponse:
    def __init__(self, code="EXCEPTION", message=None, returnobject=None):
        self.code = code
        self.message = message
        self.returnobject = returnobject

    def __iter__(self):
        yield from {
            "code": self.code,
            "message": self.message,
            "returnobject": self.returnobject
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        return {
            "code": self.code,
            "message": self.message,
            "returnobject": self.returnobject
        }