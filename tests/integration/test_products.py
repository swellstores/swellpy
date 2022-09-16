import vcr
import pytest
from datetime import datetime

@pytest.fixture
def product_keys():
    yield ['id', 'slug', 'name', 'price', 'active', 'currency']


@vcr.use_cassette('tests/vcr_cassettes/products/test-products.yml')
def test_get_products(swell):
    """Tests list all products"""

    response = swell.products.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)

@vcr.use_cassette('tests/vcr_cassettes/products/test-products-category-filter.yml')
def test_get_products_category_fitler(swell):
    """Tests listing products with category filter"""
    response = swell.products.list({ "category": "does-not-exist" })

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert len(response['results']) == 0
    assert response['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/products/test-products-date-filter.yml')
def test_get_products_date_filter(swell):
    """Tests products date filter"""

    timestamp = datetime.now()
    unfiltered = swell.products.list()
    
    filtered = swell.products.list({ 
        "active": False,
    })

    date_filtered = swell.products.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(filtered, dict)
    assert isinstance(filtered['results'], list)
    assert isinstance(filtered['count'], int)
    assert len(filtered['results']) < len(unfiltered['results'])
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0

@vcr.use_cassette('tests/vcr_cassettes/products/test-products-with-limit.yml')

def test_get_products_with_limit(swell):
    """Tests list products return limit"""

    limit = 1
    response = swell.products.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/products/test-products-expansion.yml')
def test_get_products_list_expansion(swell):
    """Tests products list expansion"""

    response = swell.products.list({"expand": ["variants"]})
    variants = response['results'][0]['variants']

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(variants['results'], list)
    assert isinstance(variants['count'], int)
    

@vcr.use_cassette('tests/vcr_cassettes/products/test-get-product.yml')
def test_get_product(product_keys, swell):
    """Tests get individual product by slug or id"""

    response = swell.products.list()
    first_product_id = response['results'][0]['id']
    first_product_slug = response['results'][0]['slug']
    
    id_response = swell.products.get(first_product_id)
    slug_response = swell.products.get(first_product_slug)

    assert set(product_keys).issubset(id_response.keys()), "All keys should be in the response"
    assert set(product_keys).issubset(slug_response.keys())


def test_fails_with_incorrect_id_get_product(swell):
    """Test fails with incorrect id type during get product"""

    with pytest.raises(TypeError):
        swell.products.get(123)


@vcr.use_cassette('tests/vcr_cassettes/products/test-get-product-expanded.yml')
def test_get_product_expanded(product_keys, swell):
    """Tests get product expanded"""

    response = swell.products.list()
    first_product_id = response['results'][0]['id']
    product_keys.append('variants')

    id_response = swell.products.get(first_product_id, { "expand": ['variants'] })

    assert set(product_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/products/test-create-product.yml')
def test_create_product(product_keys, swell):
    """Tests create new product"""
    
    new_product = {
        'name': 'New product223',
        'attributes': {
            'weight': 50
        },
        'price': 100,
        'slug': 'new-product223'
    }
    response = swell.products.create(new_product)

    assert set(product_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)


def test_fails_on_create_with_no_name(swell):
    """Test fails with no name provided on create"""
    with pytest.raises(ValueError):
        swell.products.create({"price": 20})


@vcr.use_cassette('tests/vcr_cassettes/products/test-update-product.yml')
def test_update_product(product_keys, swell):
    """Tests updating a product"""

    response = swell.products.list()
    first_product_id = response['results'][0]['id']
    
    updates = {
        "id": first_product_id,
        "name": "Updated Name",
        "price": 99
    }

    update_response = swell.products.update(updates)
    assert set(product_keys).issubset(update_response.keys())
    assert update_response["name"] == updates["name"]
    assert update_response["price"] == updates["price"]


def test_fails_with_no_id_update_product(swell):
    """Tests fails with missing id during product update"""

    with pytest.raises(Exception) as exc_info:
        swell.products.update({ "name": "updated name"})


def test_fails_with_incorrect_id_update_product(swell):
    """Tests fails with incorrect id type during product update"""

    with pytest.raises(TypeError) as exc_info:
        swell.products.update({ "name": "updated name", "id": 123})


@vcr.use_cassette('tests/vcr_cassettes/products/test-delete-product.yml')
def test_delete_product(swell, product_keys):
    """Tests deleting a product"""

    response = swell.products.list()
    first_product_id = response['results'][0]['id']

    assert isinstance(first_product_id, str)
    
    delete_response = swell.products.delete(first_product_id)
    assert set(product_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_product(swell):
    """Test fails when no id provided to delete a product"""

    with pytest.raises(Exception):
            swell.products.delete()


def test_failed_with_incorrect_id_type_delete_product(swell):
    """Test fails when incorrect id type provided to delete a product"""

    with pytest.raises(TypeError):
            swell.products.delete(132)
