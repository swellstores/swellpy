import vcr
import pytest
from datetime import datetime

@pytest.fixture
def giftcard_keys():
    yield ['id', 'amount']


@vcr.use_cassette('tests/vcr_cassettes/giftcards/test-list-giftcards.yml')
def test_list_giftcards(swell):
    """Tests list all giftcards"""

    response = swell.giftcards.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/giftcards/test-giftcards-date-filter.yml')
def test_list_giftcards_date_filter(swell):
    """Tests giftcards date filter"""

    timestamp = datetime.now()

    date_filtered = swell.giftcards.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/giftcards/test-list-giftcards-with-limit.yml')
def test_list_giftcards_with_return_limit(swell):
    """Tests list giftcards return limit"""

    limit = 1
    response = swell.giftcards.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/giftcards/test-get-giftcard.yml')
def test_get_giftcard_by_id(swell, giftcard_keys):
    """Tests get giftcard by id"""

    response = swell.giftcards.list()
    first_giftcard_id = response['results'][0]['id']
    
    id_response = swell.giftcards.get(first_giftcard_id)

    assert set(giftcard_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_giftcard(swell):
    """Test fails with incorrect id type during get giftcard"""

    with pytest.raises(TypeError):
        swell.giftcards.get(123)


@vcr.use_cassette('tests/vcr_cassettes/giftcards/test-create-giftcard.yml')
def test_create_giftcard(swell, giftcard_keys):
    """Tests create new giftcard"""

    new_giftcard = {
        'amount': 100,
    }

    response = swell.giftcards.create(new_giftcard)

    assert set(giftcard_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['amount'] == new_giftcard['amount']


def test_fails_with_no_amount(swell):
    """Tests fail when no amount is provided"""

    with pytest.raises(ValueError):
        swell.giftcards.create({})


@vcr.use_cassette('tests/vcr_cassettes/giftcards/test-update-giftcard.yml')
def test_update_giftcard(swell, giftcard_keys):
    """Tests updating a giftcard"""

    response = swell.giftcards.list()
    first_giftcard_id = response['results'][0]['id']
    
    updates = {
        "id": first_giftcard_id,
        "amount": 20
    }

    update_response = swell.giftcards.update(updates)
    assert set(giftcard_keys).issubset(update_response.keys())
    assert update_response["amount"] == updates["amount"]


def test_fails_with_no_id_update_giftcard(swell):
    """Tests fails with missing id during giftcard update"""

    with pytest.raises(Exception):
        swell.giftcards.update({ "amount": 50 })


def test_fails_with_incorrect_id_update_giftcard(swell):
    """Tests fails with incorrect id type during giftcard update"""

    with pytest.raises(TypeError):
        swell.giftcards.update({ "id": 123, "amount": 10})


@vcr.use_cassette('tests/vcr_cassettes/giftcards/test-delete-giftcard.yml')
def test_delete_giftcard(swell, giftcard_keys):
    """Tests deleting a giftcard"""

    response = swell.giftcards.list()
    first_giftcard_id = response['results'][0]['id']

    assert isinstance(first_giftcard_id, str)
    
    delete_response = swell.giftcards.delete(first_giftcard_id)
    assert set(giftcard_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_giftcard(swell):
    """Test fails when no id provided to delete a giftcard"""

    with pytest.raises(ValueError):
        swell.giftcards.delete()


def test_failed_with_incorrect_id_type_delete_giftcard(swell):
    """Test fails when incorrect id type provided to delete a giftcard"""

    with pytest.raises(TypeError):
        swell.giftcards.delete(123)
