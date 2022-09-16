import vcr
import pytest
from datetime import datetime

@pytest.fixture
def stock_keys():
    yield ['id', 'parent_id']


@vcr.use_cassette('tests/vcr_cassettes/stock/test-list-stock.yml')
def test_list_stock(swell):
    """Tests list all stock"""

    response = swell.products.stock.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/stock/test-stock-date-filter.yml')
def test_list_stock_date_filter(swell):
    """Tests stock date filter"""

    timestamp = datetime.now()

    date_filtered = swell.products.stock.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/stock/test-list-stock-with-limit.yml')
def test_list_stock_with_return_limit(swell):
    """Tests list stock return limit"""

    limit = 1
    response = swell.products.stock.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/stock/test-stock-expansion.yml')
def test_list_stock_expansion(swell):
    """Tests stock expansion param is correctly sent"""

    response = swell.products.stock.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/stock/test-get-stock.yml')
def test_get_stock_by_product_id(swell, stock_keys):
    """Tests get stock by product id"""

    response = swell.products.stock.list()
    first_product_stock_id = response['results'][0]['id']
    
    id_response = swell.products.stock.get(first_product_stock_id)

    assert set(stock_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_product_stock(swell):
    """Test fails with incorrect id type during get product stock"""

    with pytest.raises(TypeError):
        swell.products.stock.get(123)


@vcr.use_cassette('tests/vcr_cassettes/stock/test-get-stock-expanded.yml')
def test_get_product_stock_expanded(swell, stock_keys):
    """Tests get product stock expanded"""

    response = swell.products.stock.list()
    first_product_id = response['results'][0]['id']
    stock_keys.append('parent')

    id_response = swell.products.stock.get(first_product_id, { "expand": ['parent'] })

    assert set(stock_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/stock/test-create-product-stock.yml')
def test_create_product_stock(swell, stock_keys):
    """Tests create new product stock"""

    response = swell.products.list()
    first_product_id = response['results'][0]['id']
    
    new_product_stock = {
        'parent_id': first_product_id,
        'quantity': 10,
        'message': 'Received stock'
    }

    response = swell.products.stock.create(new_product_stock)

    assert set(stock_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['quantity'] == new_product_stock['quantity']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.products.stock.create({"quantity": 10})


def test_fails_with_no_quantity(swell):
    """Tests fail when no quantity is provided"""

    with pytest.raises(ValueError):
        swell.products.stock.create({"parent_id": "123"})


# @vcr.use_cassette('tests/vcr_cassettes/stock/test-update-product-stock.yml')
# def test_update_product_stock(swell, stock_keys):
#     """Tests updating an product stock"""

#     response = swell.products.stock.list()
#     first_product_stock_id = response['results'][0]['id']
    
#     updates = {
#         "id": first_product_stock_id,
#         "quantity": 99
#     }

#     update_response = swell.products.stock.update(updates)
#     assert set(stock_keys).issubset(update_response.keys())
#     assert update_response["quantity"] == updates["quantity"]


# def test_fails_with_no_id_update_product_stock(swell):
#     """Tests fails with missing id during product stock update"""

#     with pytest.raises(Exception):
#         swell.products.stock.update({ "quantity": 10 })


# def test_fails_with_incorrect_id_update_product_stock(swell):
#     """Tests fails with incorrect id type during product stock update"""

#     with pytest.raises(TypeError):
#         swell.products.stock.update({ "id": 123, "quantity": 10 })


# @vcr.use_cassette('tests/vcr_cassettes/stock/test-delete-product-stock.yml')
# def test_delete_product(swell, stock_keys):
#     """Tests deleting a product stock"""

#     response = swell.products.stock.list()
#     first_product_id = response['results'][0]['id']

#     assert isinstance(first_product_id, str)
    
#     delete_response = swell.products.stock.delete(first_product_id)
#     assert set(stock_keys).issubset(delete_response.keys()), "All keys should be in the response"


# def test_failed_with_no_id_delete_product_stock(swell):
#     """Test fails when no id provided to delete a product stock"""

#     with pytest.raises(Exception):
#         swell.products.stock.delete(123)


# def test_failed_with_incorrect_id_type_delete_product_stock(swell):
#     """Test fails when incorrect id type provided to delete an product stock"""

#     with pytest.raises(TypeError):
#         swell.products.stock.delete(123)
