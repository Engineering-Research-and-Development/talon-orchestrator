"""
Unit testing of the automatic batch processing application
"""
import unittest
from api.utils.RestResponse import RestResponse 
from run import app
import json
 
class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
            
    def test_hello(self):
        """
        Test Hello rest enpoint
        """
        response = self.app.get('/api/v1/test')


        # Deserialize the response to a RestResponse object
        rest_response = json.loads(response.text, object_hook=lambda d: RestResponse(**d))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rest_response.message, "Hello world")
 
 