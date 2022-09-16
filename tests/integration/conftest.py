import os
from dotenv import load_dotenv
import pytest
from api import Swell

load_dotenv()

SWELL_API_KEY=os.environ.get('SWELL_API_KEY', None)
SWELL_STORE_ID=os.environ.get('SWELL_STORE_ID', None)

@pytest.fixture(scope="session")
def swell():
    yield Swell({ 'store_id':SWELL_STORE_ID, 'api_key':SWELL_API_KEY})


def test_swell_init(swell):
    """ Successfully creates a new swell instance """
    assert isinstance(swell, object)


def test_init_with_base_url(swell):
    """ Initializes with base url """
    assert isinstance(swell._base_url, str)


def test_fails_swell_init_missing_key():
    """ Test fails with missing API key on init """
    with pytest.raises(Exception):
        Swell({ 'store_id':'test-store-id' })

