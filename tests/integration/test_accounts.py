import vcr
import pytest
from datetime import datetime

@pytest.fixture
def account_keys():
    yield ['id', 'type', 'name']


@vcr.use_cassette('tests/vcr_cassettes/accounts/test-accounts.yml')
def test_get_accounts(swell):
    """Tests list all accounts"""

    response = swell.accounts.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)

@vcr.use_cassette('tests/vcr_cassettes/accounts/test-accounts-date-filter.yml')
def test_get_accounts_date_filter(swell):
    """Tests accounts date filter"""

    timestamp = datetime.now()

    date_filtered = swell.accounts.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0

@vcr.use_cassette('tests/vcr_cassettes/accounts/test-accounts-with-limit.yml')
def test_get_accounts_with_return_limit(swell):
    """Tests list accounts return limit"""

    limit = 1
    response = swell.accounts.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/accounts/test-accounts-expansion.yml')
def test_get_accounts_list_expansion(swell):
    """Tests accounts expansion param is correctly sent"""

    response = swell.accounts.list({"expand": ["orders"]})
    orders = response['results'][0]['orders']

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(orders['results'], list)
    assert isinstance(orders['count'], int)
    

@vcr.use_cassette('tests/vcr_cassettes/accounts/test-get-account.yml')
def test_get_account(account_keys, swell):
    """Tests get individual account by slug or id"""

    response = swell.accounts.list()
    first_account_id = response['results'][0]['id']
    
    id_response = swell.accounts.get(first_account_id)

    assert set(account_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_account(swell):
    """Test fails with incorrect id type during get account"""

    with pytest.raises(TypeError):
        swell.accounts.get(123)


@vcr.use_cassette('tests/vcr_cassettes/accounts/test-get-account-expanded.yml')
def test_get_account_expanded(account_keys, swell):
    """Tests get account expanded"""

    response = swell.accounts.list()
    first_account_id = response['results'][0]['id']
    account_keys.append('orders')

    id_response = swell.accounts.get(first_account_id, { "expand": ['orders'] })

    assert set(account_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/accounts/test-create-account.yml')
def test_create_account(account_keys, swell):
    """Tests create new account"""
    
    new_account = {
        'type': 'individual',
        'first_name': 'test',
        'last_name': 'customer',
        'email': 'test-new4@customer.net',
        'shipping': {
            'first_name': 'test',
            'last_name': 'user',
            'address1': '14 test st',
        }
    }

    response = swell.accounts.create(new_account)

    assert set(account_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['shipping']['address1'] == new_account['shipping']['address1']


def test_fails_with_no_email(swell):
    """Tests fail when no email is provided"""
    with pytest.raises(ValueError):
        swell.accounts.create({"first_name": "user"})


@vcr.use_cassette('tests/vcr_cassettes/accounts/test-update-account.yml')
def test_update_account(account_keys, swell):
    """Tests updating a account"""

    response = swell.accounts.list()
    first_account_id = response['results'][0]['id']
    
    updates = {
        "id": first_account_id,
        "shipping": {
            "address1": "123 new address"
        },
        "first_name": "updated" 
    }

    update_response = swell.accounts.update(updates)
    assert set(account_keys).issubset(update_response.keys())
    assert update_response["first_name"] == updates["first_name"]
    assert update_response["shipping"]["address1"] == updates["shipping"]["address1"]


def test_fails_with_no_id_update_account(swell):
    """Tests fails with missing id during account update"""

    with pytest.raises(Exception):
        swell.accounts.update({ "last name": "updated name" })


def test_fails_with_incorrect_id_update_account(swell):
    """Tests fails with incorrect id type during account update"""

    with pytest.raises(TypeError):
        swell.accounts.update({ "last name": "updated name", "id": 123})


@vcr.use_cassette('tests/vcr_cassettes/accounts/test-delete-account.yml')
def test_delete_account(swell, account_keys):
    """Tests deleting a account"""

    response = swell.accounts.list()
    first_account_id = response['results'][0]['id']

    assert isinstance(first_account_id, str)
    
    delete_response = swell.accounts.delete(first_account_id)
    assert set(account_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_account(swell):
    """Test fails when no id provided to delete a account"""

    with pytest.raises(Exception):
        swell.accounts.delete()


def test_failed_with_incorrect_id_type_delete_account(swell):
    """Test fails when incorrect id type provided to delete a account"""

    with pytest.raises(TypeError):
        swell.accounts.delete(132)
