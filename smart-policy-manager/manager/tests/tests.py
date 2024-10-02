# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023
"""

import pytest
import json

from api import app
from api.utils.RestResponse import RestResponse

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello(client):
    """
       Test Hello rest enpoint
    """
    response = client.get("/api/v1/test")


    # Deserialize the response to a RestResponse object
    rest_response = json.loads(response.text, object_hook=lambda d: RestResponse(**d))
    
    assert response.status_code == 200
    assert rest_response.message == "Hello world"