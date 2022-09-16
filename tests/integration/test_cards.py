import vcr
import pytest
from datetime import datetime

@pytest.fixture
def card_keys():
    yield ['id', 'parent_id', 'token']


@vcr.use_cassette('tests/vcr_cassettes/cards/test-list-cards.yml')
def test_list_cards(swell):
    """Tests list all cards"""

    response = swell.accounts.cards.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/cards/test-cards-date-filter.yml')
def test_list_cards_date_filter(swell):
    """Tests cards date filter"""

    timestamp = datetime.now()

    date_filtered = swell.accounts.cards.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/cards/test-list-cards-with-limit.yml')
def test_list_cards_with_return_limit(swell):
    """Tests list cards return limit"""

    limit = 1
    response = swell.accounts.cards.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/cards/test-cards-expansion.yml')
def test_list_cards_expansion(swell):
    """Tests cards expansion param is correctly sent"""

    response = swell.accounts.cards.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/cards/test-get-cards.yml')
def test_get_cards_by_id(swell, card_keys):
    """Tests get cards by id"""

    response = swell.accounts.cards.list()
    first_account_id = response['results'][0]['id']
    
    id_response = swell.accounts.cards.get(first_account_id)

    assert set(card_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_account_cards(swell):
    """Test fails with incorrect id type during get account cards"""

    with pytest.raises(TypeError):
        swell.accounts.cards.get(123)


@vcr.use_cassette('tests/vcr_cassettes/cards/test-get-cards-expanded.yml')
def test_get_account_cards_expanded(swell, card_keys):
    """Tests get account cards expanded"""

    response = swell.accounts.cards.list()
    first_account_id = response['results'][0]['id']
    card_keys.append('parent')

    id_response = swell.accounts.cards.get(first_account_id, { "expand": ['parent'] })

    assert set(card_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/cards/test-create-account-card.yml')
def test_create_account_card(swell, card_keys):
    """Tests create new account card"""

    response = swell.accounts.list()
    first_account_id = response['results'][0]['id']
    
    new_account_card = {
        'parent_id': first_account_id,
        'token': 'xyz'
    }

    response = swell.accounts.cards.create(new_account_card)

    assert set(card_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['token'] == new_account_card['token']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.accounts.cards.create({"token": 'xyz'})

def test_fails_with_no_token(swell):
    """Tests fail when no token is provided"""

    with pytest.raises(ValueError):
        swell.accounts.cards.create({"parent_id": "123"})


@vcr.use_cassette('tests/vcr_cassettes/cards/test-update-account-card.yml')
def test_update_account_card(swell, card_keys):
    """Tests updating an account card"""

    response = swell.accounts.cards.list()
    first_account_card_id = response['results'][0]['id']
    
    updates = {
        "id": first_account_card_id,
        "token": "abc"
    }

    update_response = swell.accounts.cards.update(updates)
    assert set(card_keys).issubset(update_response.keys())
    assert update_response["token"] == updates["token"]


def test_fails_with_no_id_update_account_card(swell):
    """Tests fails with missing id during account card update"""

    with pytest.raises(Exception):
        swell.accounts.cards.update({ "token": "ghi" })


def test_fails_with_incorrect_id_update_account_card(swell):
    """Tests fails with incorrect id type during account card update"""

    with pytest.raises(TypeError):
        swell.accounts.cards.update({ "id": 123, "token": "ghi"})


@vcr.use_cassette('tests/vcr_cassettes/cards/test-delete-account-card.yml')
def test_delete_account(swell, card_keys):
    """Tests deleting an account card"""

    response = swell.accounts.cards.list()
    first_account_card_id = response['results'][0]['id']

    assert isinstance(first_account_card_id, str)
    
    delete_response = swell.accounts.cards.delete(first_account_card_id)
    assert set(card_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_account_card(swell):
    """Test fails when no id provided to delete a account card"""

    with pytest.raises(Exception):
        swell.accounts.cards.delete(123)


def test_failed_with_incorrect_id_type_delete_account_card(swell):
    """Test fails when incorrect id type provided to delete an account card"""

    with pytest.raises(TypeError):
        swell.accounts.cards.delete(123)
