import vcr
import pytest
from datetime import datetime

@pytest.fixture
def coupon_keys():
    yield ['id', 'name']


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-list-coupons.yml')
def test_list_coupons(swell):
    """Tests list all coupons"""

    response = swell.coupons.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-coupons-date-filter.yml')
def test_list_coupons_date_filter(swell):
    """Tests coupons date filter"""

    timestamp = datetime.now()

    date_filtered = swell.coupons.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-list-coupons-with-limit.yml')
def test_list_coupons_with_return_limit(swell):
    """Tests list coupons return limit"""

    limit = 1
    response = swell.coupons.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/coupons/test-coupons-expansion.yml')
def test_list_coupons_expansion(swell):
    """Tests coupons expansion param is correctly sent"""

    response = swell.coupons.list({"expand": ["orders"]})
    orders = response['results'][0]['orders']

    assert isinstance(orders, dict)


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-get-coupon.yml')
def test_get_coupon_by_id(swell, coupon_keys):
    """Tests get coupon by id"""

    response = swell.coupons.list()
    first_coupon_id = response['results'][0]['id']
    
    id_response = swell.coupons.get(first_coupon_id)

    assert set(coupon_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_coupon(swell):
    """Test fails with incorrect id type during get coupon"""

    with pytest.raises(TypeError):
        swell.coupons.get(123)


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-get-coupon-expanded.yml')
def test_get_coupon_expanded(swell, coupon_keys):
    """Tests get coupon expanded"""

    response = swell.coupons.list()
    first_coupon_id = response['results'][0]['id']

    id_response = swell.coupons.get(first_coupon_id, { "expand": ['orders'] })

    assert set(coupon_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-create-coupon.yml')
def test_create_coupon(swell, coupon_keys):
    """Tests create new coupon"""

    new_coupon = {
        'name': '99% Off Sale',
        'active': False,
        'discounts': {
            'value_type': 'percent',
            'value_percent': 90
        },
        'codes': [{ 'code': 'SAVE98' }]
    }

    response = swell.coupons.create(new_coupon)

    assert set(coupon_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['name'] == new_coupon['name']


def test_fails_with_no_name(swell):
    """Tests fail when no name is provided"""

    with pytest.raises(ValueError):
        swell.coupons.create({
            'discounts': {
                'value_type': 'percent',
                'value_percent': 90
            },
            'codes': [{ 'code': 'SAVE90' }]
        })

def test_fails_with_no_discounts(swell):
    """Tests fail when no discounts are provided"""

    with pytest.raises(ValueError):
        swell.coupons.create({
            'codes': [{ 'code': 'SAVE90' }],
            'name': 'test'
        })

def test_fails_with_no_codes(swell):
    """Tests fail when no codes are provided"""

    with pytest.raises(ValueError):
        swell.coupons.create({
            'name': 'test',
            'discounts': {
                'value_type': 'percent',
                'value_percent': 90
            }
        })


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-update-coupon.yml')
def test_update_coupon(swell, coupon_keys):
    """Tests updating a coupon"""

    response = swell.coupons.list()
    first_coupon_id = response['results'][0]['id']
    
    updates = {
        "id": first_coupon_id,
        "name": "new coupon name"
    }

    update_response = swell.coupons.update(updates)
    assert set(coupon_keys).issubset(update_response.keys())
    assert update_response["name"] == updates["name"]


def test_fails_with_no_id_update_coupon(swell):
    """Tests fails with missing id during coupon update"""

    with pytest.raises(Exception):
        swell.coupons.update({ "coupon1": "123 test" })


def test_fails_with_incorrect_id_update_coupon(swell):
    """Tests fails with incorrect id type during coupon update"""

    with pytest.raises(TypeError):
        swell.coupons.update({ "id": 123, "coupon1": "123 test"})


@vcr.use_cassette('tests/vcr_cassettes/coupons/test-delete-coupon.yml')
def test_delete_coupon(swell, coupon_keys):
    """Tests deleting a coupon"""

    response = swell.coupons.list()
    first_coupon_id = response['results'][0]['id']

    assert isinstance(first_coupon_id, str)
    
    delete_response = swell.coupons.delete(first_coupon_id)
    assert set(coupon_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_coupon(swell):
    """Test fails when no id provided to delete a coupon"""

    with pytest.raises(ValueError):
        swell.coupons.delete()


def test_failed_with_incorrect_id_type_delete_coupon(swell):
    """Test fails when incorrect id type provided to delete a coupon"""

    with pytest.raises(TypeError):
        swell.coupons.delete(123)
