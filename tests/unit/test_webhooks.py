from asyncio import events
import unittest
from unittest.mock import MagicMock
from api.models.webhooks import Webhooks
from api.models.base import Base


class TestEvents(unittest.TestCase):
    @classmethod
    def setUp(self):
        class SessionMock:
            def __init__(self):
                self.get = MagicMock()

        class SwellMock:
            def __init__(self):
                self._session = SessionMock()
                self._base_url = 'https://store_id:api_key'

        global webhook_model, swell

        swell = SwellMock()
        webhook_model = Webhooks(swell)


    def test_webhook_list_events(self):
        """ Test webhook list events activity"""

        params = {'sort': 'asc'}
        webhook_model.list_events(params)
        webhook_model._swell._session.get.assert_called_once_with(url='https://store_id:api_key/events:webhooks/', params={'sort': 'asc'})