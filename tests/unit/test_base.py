import unittest
from unittest.mock import MagicMock
from api.models.base import Base
class TestBaseClass(unittest.TestCase):

    @classmethod
    def setUp(self):
        class SessionMock:
            def __init__(self):
                self.get = MagicMock()
                self.put = MagicMock()
                self.post = MagicMock()
                self.delete = MagicMock()

        class SwellMock:
            def __init__(self):
                self._session = SessionMock()
                self._base_url = 'https://store_id:api_key'

        global base_model, name, endpoint, required_fields, swell

        name = 'tester'
        endpoint = 'mock'
        required_fields = ['name', 'value']
        swell = SwellMock()
        base_model = Base(swell, name, endpoint=endpoint, required_fields=required_fields)
        

    def test_base_model_init(self):
        """Tests base model initialization"""

        assert isinstance(base_model, object)
        assert base_model.name == name
        assert base_model.endpoint == endpoint
        assert base_model.required_fields == required_fields
        assert base_model._swell == swell

        
    def test_base_model_default_endpoint(self):
        """Tests base model default endpoint"""

        new_model = Base(swell, name, required_fields=required_fields)

        assert new_model.endpoint == name


    def test_list_method_mock(self):
        """Tests list method called with correct arguments"""

        params = {'sort': 'asc'}
        base_model.list(params)
        base_model._swell._session.get.assert_called_once_with(url='https://store_id:api_key/mock', params=params)


    def test_get_method_mock(self):
        """Tests get method called with correct arguments"""

        id = 'abc123'
        params = {'sort': 'asc'}
        base_model.get(id, params)
        base_model._swell._session.get.assert_called_once_with(url=f'https://store_id:api_key/mock/{id}', params=params)


    def test_get_fails_with_no_id(self):
        """Tests get method failure with no id"""

        with self.assertRaises(TypeError):
            base_model.get(123)


    def test_create_fails_with_missing_required_field(self):
        """ Tests create method failure with missing required field"""

        with self.assertRaises(ValueError):
            base_model.create({'name': 'test'}) #missing 'value' required field


    def test_update_method_mock(self):
        """Tests update method called with correct arguments"""

        id = 'abc123'
        params = {'id': id, 'name': 'test'}
        base_model.update(params)
        base_model._swell._session.put.assert_called_once_with(url=f'https://store_id:api_key/mock/{id}', json=params)


    def test_update_fails_with_no_id(self):
        """ Tests update method failure with missing id"""

        with self.assertRaises(Exception):
            base_model.update({'some': 'update'})


    def test_update_fails_with_incorrect_id_type(self):
        """ Tests update method failure with incorrect id type"""

        with self.assertRaises(TypeError):
            base_model.update({'id': 123, 'some': 'update'})


    def test_delete_method_mock(self):
        """Tests delete method called with correct arguments"""

        id = 'abc123'
        base_model.delete(id)
        base_model._swell._session.delete.assert_called_once_with(url=f'https://store_id:api_key/mock/{id}')


    def test_delete_fails_with_no_id(self):
        """ Tests delete method failure with missing id"""

        with self.assertRaises(Exception):
            base_model.delete()

    def test_delete_fails_with_incorrect_id_type(self):
        """ Tests delete method failure with incorrect id type"""

        with self.assertRaises(TypeError):
            base_model.delete(123)


if __name__ == '__main__':
    unittest.main()