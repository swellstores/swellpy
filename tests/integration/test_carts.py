import vcr
import pytest
from datetime import datetime


@pytest.fixture
def cart_keys():
    yield ['id', 'billing', 'shipping', 'grand_total']


@vcr.use_cassette('tests/vcr_cassettes/carts/test-list-carts.yml')
def test_get_carts(swell):
    """Tests list all carts"""

    response = swell.carts.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/carts/test-carts-date-filter.yml')
def test_get_carts_date_filter(swell):
    """Tests carts date filter"""

    timestamp = datetime.now()

    date_filtered = swell.carts.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0

@vcr.use_cassette('tests/vcr_cassettes/carts/test-carts-with-limit.yml')
def test_get_carts_with_return_limit(swell):
    """Tests list carts return limit"""

    limit = 1
    response = swell.carts.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/carts/test-carts-expansion.yml')
def test_list_carts_with_expansion(swell):
    """Tests carts list expansion"""

    response = swell.carts.list({"expand": ["account"]})
    account = response['results'][0]['account']

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(account, dict) or account == None
    

@vcr.use_cassette('tests/vcr_cassettes/carts/test-get-cart.yml')
def test_get_cart(swell, cart_keys):
    """Tests get individual cart by id"""

    response = swell.carts.list()
    first_cart_id = response['results'][0]['id']
    
    response = swell.carts.get(first_cart_id)

    assert set(cart_keys).issubset(response.keys()), "All keys should be in the response"
    assert set(cart_keys).issubset(response.keys())


def test_fails_with_incorrect_id_get_cart(swell):
    """Test fails with incorrect id type during get cart"""

    with pytest.raises(TypeError):
        swell.carts.get(123)


@vcr.use_cassette('tests/vcr_cassettes/carts/test-get-cart-expanded.yml')
def test_get_cart_expanded(swell, cart_keys):
    """Tests get cart expanded"""

    response = swell.carts.list()
    first_cart_id = response['results'][0]['id']
    cart_keys.append('account')

    id_response = swell.carts.get(first_cart_id, { "expand": ['account'] })

    assert set(cart_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/carts/test-create-cart.yml')
def test_create_cart(swell, cart_keys):
    """Tests create new cart"""
    
    new_cart = {
        "shipping": {
            "name":"test user",
            "first_name":"test",
            "last_name":"user",
            "address1": "2000 Tester St"
        }
    }
    response = swell.carts.create(new_cart)
    assert set(cart_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)


@vcr.use_cassette('tests/vcr_cassettes/carts/test-update-cart.yml')
def test_update_cart(swell, cart_keys):
    """Tests updating a cart"""

    response = swell.carts.list()
    first_cart_id = response['results'][0]['id']
    
    updates = {
        "id": first_cart_id,
        "active": False,
        "checkout_url": "http://testurl.com"
    }

    update_response = swell.carts.update(updates)
    assert set(cart_keys).issubset(update_response.keys())
    assert update_response["active"] == updates["active"]
    assert update_response["checkout_url"] == updates["checkout_url"]


def test_fails_with_no_id_update_cart(swell):
    """Tests fails with missing id during cart update"""

    with pytest.raises(Exception):
        swell.carts.update({ "active": False })


def test_fails_with_incorrect_id_update_cart(swell):
    """Tests fails with incorrect id type during cart update"""

    with pytest.raises(TypeError):
        swell.carts.update({ "name": "updated name", "id": 123})


@vcr.use_cassette('tests/vcr_cassettes/carts/test-delete-cart.yml')
def test_delete_cart(swell, cart_keys):
    """Tests deleting a cart"""

    response = swell.carts.list()
    first_cart_id = response['results'][0]['id']

    assert isinstance(first_cart_id, str)
    
    delete_response = swell.carts.delete(first_cart_id)
    assert set(cart_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_cart(swell):
    """Test fails when no id provided to delete a cart"""

    with pytest.raises(ValueError):
            swell.carts.delete()


def test_failed_with_incorrect_id_type_delete_cart(swell):
    """Test fails when incorrect id type provided to delete a cart"""

    with pytest.raises(TypeError):
            swell.carts.delete(132)
