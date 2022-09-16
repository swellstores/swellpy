from asyncio import events
import unittest
from api.models.events import Events
from api.models.base import Base

class TestEvents(unittest.TestCase):

    def setUp(self):
        global events_model
        events_model = Events(Base)

    def test_fails_with_create_method(self):
        """ Test fails when create method is called"""
        with self.assertRaises(NotImplementedError):
            events_model.create({'new': 'event'})

    def test_fails_with_update_method(self):
        """ Test fails when update method is called"""
        with self.assertRaises(NotImplementedError):
            events_model.update({'id': '123', 'new': 'event'})

    def test_fails_with_delete_method(self):
        """ Test fails when delete method is called"""
        with self.assertRaises(NotImplementedError):
            events_model.delete('123')


if __name__ == '__main__':
    unittest.main()