import vcr
import pytest
from datetime import datetime

@pytest.fixture
def use_keys():
    yield ['id', 'code', 'parent_id', 'code_id']


@vcr.use_cassette('tests/vcr_cassettes/uses/test-list-uses.yml')
def test_list_uses(swell):
    """Tests list all uses"""

    response = swell.coupons.uses.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/uses/test-uses-date-filter.yml')
def test_list_uses_date_filter(swell):
    """Tests uses date filter"""

    timestamp = datetime.now()

    date_filtered = swell.coupons.uses.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/uses/test-list-uses-with-limit.yml')
def test_list_uses_with_return_limit(swell):
    """Tests list uses return limit"""

    limit = 1
    response = swell.coupons.uses.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/uses/test-uses-expansion.yml')
def test_list_uses_expansion(swell):
    """Tests uses expansion param is correctly sent"""

    response = swell.coupons.uses.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/uses/test-get-uses.yml')
def test_get_uses_by_coupon_id(swell, use_keys):
    """Tests get uses by coupon id"""

    response = swell.coupons.uses.list()
    first_coupon_id = response['results'][0]['id']
    
    id_response = swell.coupons.uses.get(first_coupon_id)

    assert set(use_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_coupon_uses(swell):
    """Test fails with incorrect id type during get coupon uses"""

    with pytest.raises(TypeError):
        swell.coupons.uses.get(123)


@vcr.use_cassette('tests/vcr_cassettes/uses/test-get-uses-expanded.yml')
def test_get_coupon_uses_expanded(swell, use_keys):
    """Tests get coupon uses expanded"""

    response = swell.coupons.uses.list()
    first_coupon_id = response['results'][0]['id']
    use_keys.append('parent')

    id_response = swell.coupons.uses.get(first_coupon_id, { "expand": ['parent'] })

    assert set(use_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/uses/test-create-coupon-use.yml')
def test_create_coupon_use(swell, use_keys):
    """Tests create new coupon use"""

    response = swell.coupons.list({ 'expand': 'codes'})
    first_coupon = response['results'][0]
    coupon_code = first_coupon['codes']['results'][0]
    
    new_coupon_use = {
        'parent_id': first_coupon['id'],
        'code': coupon_code['code'],
        'code_id': coupon_code['id']

    }

    response = swell.coupons.uses.create(new_coupon_use)

    assert set(use_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['parent_id'] == new_coupon_use['parent_id']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.coupons.uses.create({"code": "123", "code_id": "123"})

def test_fails_with_no_count(swell):
    """Tests fail when no code_id is provided"""

    with pytest.raises(ValueError):
        swell.coupons.uses.create({"parent_id": "123", "code": "123"})


@vcr.use_cassette('tests/vcr_cassettes/uses/test-delete-coupon-use.yml')
def test_delete_coupon_use(swell, use_keys):
    """Tests deleting an coupon use"""

    response = swell.coupons.uses.list()
    first_coupon_use_id = response['results'][0]['id']

    assert isinstance(first_coupon_use_id, str)
    
    delete_response = swell.coupons.uses.delete(first_coupon_use_id)
    assert set(use_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_coupon_use(swell):
    """Test fails when no id provided to delete a coupon use"""

    with pytest.raises(Exception):
        swell.coupons.uses.delete(123)


def test_failed_with_incorrect_id_type_delete_coupon_use(swell):
    """Test fails when incorrect id type provided to delete an coupon use"""

    with pytest.raises(TypeError):
        swell.coupons.uses.delete(123)
