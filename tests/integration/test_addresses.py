import vcr
import pytest
from datetime import datetime

@pytest.fixture
def address_keys():
    yield ['id', 'name', 'address1']


@vcr.use_cassette('tests/vcr_cassettes/addresses/test-list-addresses.yml')
def test_list_addresses(swell):
    """Tests list all addresses"""

    response = swell.addresses.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/addresses/test-addresses-date-filter.yml')
def test_list_addresses_date_filter(swell):
    """Tests addresses date filter"""

    timestamp = datetime.now()

    date_filtered = swell.addresses.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/addresses/test-list-addresses-with-limit.yml')
def test_list_addresses_with_return_limit(swell):
    """Tests list addresses return limit"""

    limit = 1
    response = swell.addresses.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/addresses/test-addresses-expansion.yml')
def test_list_addresses_expansion(swell):
    """Tests addresses expansion param is correctly sent"""

    response = swell.addresses.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/addresses/test-get-addresses.yml')
def test_get_addresses_by_account_id(swell, address_keys):
    """Tests get addresses by account id"""

    response = swell.addresses.list()
    first_account_id = response['results'][0]['id']
    
    id_response = swell.addresses.get(first_account_id)

    assert set(address_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_account_addresses(swell):
    """Test fails with incorrect id type during get account addresses"""

    with pytest.raises(TypeError):
        swell.addresses.get(123)


@vcr.use_cassette('tests/vcr_cassettes/addresses/test-get-addresses-expanded.yml')
def test_get_account_addresses_expanded(swell, address_keys):
    """Tests get account addresses expanded"""

    response = swell.addresses.list()
    first_account_id = response['results'][0]['id']
    address_keys.append('parent')

    id_response = swell.addresses.get(first_account_id, { "expand": ['parent'] })

    assert set(address_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/addresses/test-create-account-address.yml')
def test_create_account_address(swell, address_keys):
    """Tests create new account address"""

    response = swell.addresses.list()
    first_account_id = response['results'][0]['id']
    
    new_account_address = {
        'parent_id': first_account_id,
        'first_name': 'Adoring',
        'last_name': 'Fan',
        'address1': '123 Breezehome St',
        'city': 'Whiterun',
        'country': 'US'
    }

    response = swell.addresses.create(new_account_address)

    assert set(address_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['address1'] == new_account_address['address1']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.addresses.create({"address1": "123 test st."})

def test_fails_with_no_address1(swell):
    """Tests fail when no address1 is provided"""

    with pytest.raises(ValueError):
        swell.addresses.create({"parent_id": "123"})



@vcr.use_cassette('tests/vcr_cassettes/addresses/test-update-account-address.yml')
def test_update_account_address(swell, address_keys):
    """Tests updating an account address"""

    response = swell.addresses.list()
    first_account_address_id = response['results'][0]['id']
    
    updates = {
        "id": first_account_address_id,
        "address1": "new address 321"
    }

    update_response = swell.addresses.update(updates)
    assert set(address_keys).issubset(update_response.keys())
    assert update_response["address1"] == updates["address1"]


def test_fails_with_no_id_update_account_address(swell):
    """Tests fails with missing id during account address update"""

    with pytest.raises(Exception):
        swell.addresses.update({ "address1": "123 test" })


def test_fails_with_incorrect_id_update_account_address(swell):
    """Tests fails with incorrect id type during account address update"""

    with pytest.raises(TypeError):
        swell.addresses.update({ "id": 123, "address1": "123 test"})


@vcr.use_cassette('tests/vcr_cassettes/addresses/test-delete-account-address.yml')
def test_delete_account(swell, address_keys):
    """Tests deleting an account address"""

    response = swell.addresses.list()
    first_account_id = response['results'][0]['id']

    assert isinstance(first_account_id, str)
    
    delete_response = swell.addresses.delete(first_account_id)
    assert set(address_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_account_address(swell):
    """Test fails when no id provided to delete a account address"""

    with pytest.raises(Exception):
        swell.addresses.delete(123)


def test_failed_with_incorrect_id_type_delete_account_address(swell):
    """Test fails when incorrect id type provided to delete an account address"""

    with pytest.raises(TypeError):
        swell.addresses.delete(123)
