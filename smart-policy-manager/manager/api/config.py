# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023
"""

import os, random, string
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class BaseConfig():    
    PORT = os.getenv('PORT', None)
   
cat_metrics_dataset = "/api/Models_tassonomy_metrics_2.csv"
algos_dataset = "/api/Models_tassonomy_metrics.csv"
categories = ["Quality", "Speed of execution", "Energy efficiency", "Cost reduction"]
