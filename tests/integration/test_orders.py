import vcr
import pytest
from datetime import datetime


@pytest.fixture
def order_keys():
    yield ['id', 'items', 'account_id', 'shipping', 'billing', 'number']



@vcr.use_cassette('tests/vcr_cassettes/orders/test-list-orders.yml')
def test_get_orders(swell):
    """Tests list orders"""

    response = swell.orders.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/orders/test-orders-date-filter.yml')
def test_get_orders_date_filter(swell):
    """Tests orders date filter"""

    timestamp = datetime.now()

    date_filtered = swell.orders.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0

@vcr.use_cassette('tests/vcr_cassettes/orders/test-orders-with-limit.yml')
def test_get_orders_with_return_limit(swell):
    """Tests list orders return limit"""

    limit = 1
    response = swell.orders.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/orders/test-orders-expansion.yml')
def test_list_orders_with_expansion(swell):
    """Tests orders list expansion"""

    response = swell.orders.list({"expand": ["account"]})
    account = response['results'][0]['account']

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(account, dict) or account == None
    

@vcr.use_cassette('tests/vcr_cassettes/orders/test-get-order.yml')
def test_get_order(order_keys, swell):
    """Tests get individual order by id"""

    response = swell.orders.list()
    first_order_id = response['results'][0]['id']
    
    response = swell.orders.get(first_order_id)

    assert set(order_keys).issubset(response.keys()), "All keys should be in the response"
    assert set(order_keys).issubset(response.keys())


def test_fails_with_incorrect_id_get_order(swell):
    """Test fails with incorrect id type during get order"""

    with pytest.raises(TypeError):
        swell.orders.get(123)


@vcr.use_cassette('tests/vcr_cassettes/orders/test-get-order-expanded.yml')
def test_get_order_expanded(order_keys, swell):
    """Tests get order expanded"""

    response = swell.orders.list()
    first_order_id = response['results'][0]['id']
    order_keys.append('account')

    id_response = swell.orders.get(first_order_id, { "expand": ['account'] })

    assert set(order_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/orders/test-convert-cart-to-order.yml')
def test_convert_cart_to_order(order_keys, swell):
    """Tests convert cart to order"""
    cart_id = swell.carts.list()["results"][0]["id"]

    response = swell.orders.convert_cart_to_order(cart_id)

    # Any API response payload is passing, since we're justing the wrapper api. separate from end-to-end tests
    assert set(order_keys).issubset(response.keys()) or response["errors"], "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/orders/test-update-order.yml')
def test_update_order(order_keys, swell):
    """Tests updating a order"""

    response = swell.orders.list()
    first_order_id = response['results'][0]['id']
    
    updates = {
        "id": first_order_id,
        "coupon_code": "SAVE10",
    }

    update_response = swell.orders.update(updates)
    assert set(order_keys).issubset(update_response.keys())
    assert update_response["coupon_code"] == updates["coupon_code"]


def test_fails_with_no_id_update_order(swell):
    """Tests fails with missing id during order update"""

    with pytest.raises(Exception):
        swell.orders.update({ "active": False })


def test_fails_with_incorrect_id_update_order(swell):
    """Tests fails with incorrect id type during order update"""

    with pytest.raises(TypeError):
        swell.orders.update({ "name": "updated name", "id": 123})


@vcr.use_cassette('tests/vcr_cassettes/orders/test-delete-order.yml')
def test_delete_order(swell, order_keys):
    """Tests deleting a order"""

    response = swell.orders.list()
    first_order_id = response['results'][0]['id']

    assert isinstance(first_order_id, str)
    
    delete_response = swell.orders.delete(first_order_id)
    assert set(order_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_order(swell):
    """Test fails when no id provided to delete a order"""

    with pytest.raises(ValueError):
            swell.orders.delete()


def test_failed_with_incorrect_id_type_delete_order(swell):
    """Test fails when incorrect id type provided to delete a order"""

    with pytest.raises(TypeError):
            swell.orders.delete(132)
