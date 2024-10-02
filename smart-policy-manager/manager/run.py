# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023
"""
import pytest
import unittest
import click

from api import app
import json

from api.utils.RestResponse import RestResponse 
from api.utils.custom_json_encoder import CustomJSONEncoder 
from api.utils.swagger import configure_swagger

app.json_encoder = CustomJSONEncoder

# Configure Swagger
configure_swagger(app)

@app.shell_context_processor
def make_shell_context():
    return {"app": app}

@app.cli.command("tests")
@click.argument("option", required=False)
def run_test_with_option(option: str = None):
    if option is None:
        raise SystemExit(pytest.main(["-v", "tests/tests.py"]))
    
@app.cli.command("unittests")
def run_unittests(pattern: str = None):
    tests = unittest.TestLoader().discover("tests", pattern="test_*.py")
    unittest.TextTestRunner().run(tests)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")