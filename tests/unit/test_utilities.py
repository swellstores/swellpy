import unittest
from unittest.mock import MagicMock
from urllib.error import HTTPError
from api.utilities import handle_requests_response
from mock import patch
from requests.exceptions import HTTPError
class TestUtils(unittest.TestCase):

    @classmethod
    def setUp(cls):
        global ResponseObj
        global swell

        class Request():
            def __init__(self):
                self.method = "GET"
        class ResponseObj():
            def __init__(self, json_data=None, status_code=200):
                self.status_code = status_code
                self.data = json_data
                self.request = Request()
                self.url = 'abc/def'
                self.reason = 'Default'

            def json(self):
                return self.data

        class SwellMock:
            def __init__(self):
                self.logger = MagicMock()

        swell = SwellMock()
        
    def test_handle_invalid_response(self):
        """Test raises exception with invalid or null response"""
        empty_response = ResponseObj()

        with self.assertRaises(Exception):
            handle_requests_response(swell, empty_response)

    def test_handle_error_response(self):
        """Test raises exception with error response"""

        error_response = ResponseObj({ 
            "errors": {
                "slug": "errorinfo"
            }})

        handle_requests_response(swell, error_response)
        swell.logger.debug.assert_called_with({"slug": "errorinfo"})

    def test_handle_json_response(self):

        json_response = ResponseObj({
            "some": "data",
        })

        res = handle_requests_response(swell, json_response)

        self.assertEqual(type(res), dict)

    def test_404_response(self):

        json_response = ResponseObj({
            "some": "data",
        }, 400)


        with self.assertRaises(HTTPError):
            handle_requests_response(swell, json_response)


if __name__ == '__main__':
    unittest.main()