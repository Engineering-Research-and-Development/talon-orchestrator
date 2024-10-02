# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 
"""

from flask_restx import Api, Resource, fields
from flask import request
# from .api_models import *
from .config import BaseConfig
from api.utils.RestResponse import RestResponse
# from api.utils.swagger_models import DictItem
import os
import json
from bson import ObjectId
from .smart import get_available_algos_based_on_task, LinearProgrammingExample, get_execution_config

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

rest_api = Api(version="1.0.0", title="Talon API")
api = rest_api
ns = rest_api.namespace('smart-policy-manager', description='')



"""
    Flask-Restx models for api request and response data
"""
@rest_api.route('/api/v1/test')
class Test(Resource):
    @rest_api.expect(validate=True)
    def get(self):
        """
            test rest endpoint.
        """
        return RestResponse(code="SUCCESS", message="Hello world").to_json()


parameters = api.model(
    'PARAMETERS',
    {
        "Quality": fields.Integer(min=0, max=100),
        "Speed of execution": fields.Integer(min=0, max=100),
        "Energy efficiency": fields.Integer(min=0, max=100),
        "Cost reduction": fields.Integer(min=0, max=100),
    }
)


@ns.route('/choose_task')
@ns.response(404, 'Not found')
class Choice(Resource):

    resource_fields = api.model('Resource', {
        'task': fields.String("Time series interpolation"),
        'parameters': fields.Nested(parameters)
    })
    
    @ns.expect(resource_fields)
    @ns.doc('choose_task')
    def post(self):
        '''Based on task and desired execution parameters, get algorithm choice'''
                
        algos = get_available_algos_based_on_task(rest_api.payload['task'])

        algo = LinearProgrammingExample(algos=algos, parameters=rest_api.payload['parameters'])

        return get_execution_config(algo=algo)
