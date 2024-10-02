# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023
"""

import os, json

from flask import Flask
from flask_cors import CORS

from .routes import rest_api

app = Flask(__name__)

app.config.from_object('api.config.BaseConfig')

rest_api.init_app(app)
CORS(app)
