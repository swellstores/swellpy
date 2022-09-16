import unittest
from api.utilities import handle_requests_response

class TestUtils(unittest.TestCase):

    @classmethod
    def setUp(self):
        global RequestsObj

        class RequestsObj():
            def __init__(self, json_data=None):
                self.data = json_data

            def json(self):
                return self.data
        

    def test_handle_invalid_response(self):
        """Test raises exception with invalid or null response"""
        empty_response = RequestsObj()

        with self.assertRaises(Exception):
            handle_requests_response(empty_response)


    def test_handle_error_response(self):
        """Test raises exception with error response"""

        error_response = RequestsObj({ 
            "errors": {
                "slug": "errorinfo"
            }})

        with self.assertRaises(Exception):
            handle_requests_response(error_response)


    def test_handle_json_response(self):

        json_response = RequestsObj({
            "some": "data"
        })

        res = handle_requests_response(json_response)

        self.assertEqual(type(res), dict)


if __name__ == '__main__':
    unittest.main()