import vcr
import pytest
from datetime import datetime

@pytest.fixture
def use_keys():
    yield ['id', 'parent_id']


@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-list-uses.yml')
def test_list_uses(swell):
    """Tests list all uses"""

    response = swell.promotions.uses.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-uses-date-filter.yml')
def test_list_uses_date_filter(swell):
    """Tests uses date filter"""

    timestamp = datetime.now()

    date_filtered = swell.promotions.uses.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-list-uses-with-limit.yml')
def test_list_uses_with_return_limit(swell):
    """Tests list uses return limit"""

    limit = 1
    response = swell.promotions.uses.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-uses-expansion.yml')
def test_list_uses_expansion(swell):
    """Tests uses expansion param is correctly sent"""

    response = swell.promotions.uses.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-get-uses.yml')
def test_get_uses_by_promotion_id(swell, use_keys):
    """Tests get uses by promotion id"""

    response = swell.promotions.uses.list()
    first_promotion_id = response['results'][0]['id']
    
    id_response = swell.promotions.uses.get(first_promotion_id)

    assert set(use_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_promotion_uses(swell):
    """Test fails with incorrect id type during get promotion uses"""

    with pytest.raises(TypeError):
        swell.promotions.uses.get(123)


@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-get-uses-expanded.yml')
def test_get_promotion_uses_expanded(swell, use_keys):
    """Tests get promotion uses expanded"""

    response = swell.promotions.uses.list()
    first_promotion_id = response['results'][0]['id']
    use_keys.append('parent')

    id_response = swell.promotions.uses.get(first_promotion_id, { "expand": ['parent'] })

    assert set(use_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-create-promotion-use.yml')
def test_create_promotion_use(swell, use_keys):
    """Tests create new promotion use"""

    response = swell.promotions.list({ 'expand': 'codes'})
    first_promotion = response['results'][0]
    
    new_promotion_use = {
        'parent_id': first_promotion['id']

    }

    response = swell.promotions.uses.create(new_promotion_use)

    assert set(use_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['parent_id'] == new_promotion_use['parent_id']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.promotions.uses.create({})


@vcr.use_cassette('tests/vcr_cassettes/promotion-uses/test-delete-promotion-use.yml')
def test_delete_promotion_use(swell, use_keys):
    """Tests deleting an promotion use"""

    response = swell.promotions.uses.list()
    first_promotion_use_id = response['results'][0]['id']

    assert isinstance(first_promotion_use_id, str)
    
    delete_response = swell.promotions.uses.delete(first_promotion_use_id)
    assert set(use_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_promotion_use(swell):
    """Test fails when no id provided to delete a promotion use"""

    with pytest.raises(Exception):
        swell.promotions.uses.delete(123)


def test_failed_with_incorrect_id_type_delete_promotion_use(swell):
    """Test fails when incorrect id type provided to delete an promotion use"""

    with pytest.raises(TypeError):
        swell.promotions.uses.delete(123)
