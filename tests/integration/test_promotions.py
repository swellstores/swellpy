import vcr
import pytest
from datetime import datetime

@pytest.fixture
def promotion_keys():
    yield ['id', 'name']


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-list-promotions.yml')
def test_list_promotions(swell):
    """Tests list all promotions"""

    response = swell.promotions.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-promotions-date-filter.yml')
def test_list_promotions_date_filter(swell):
    """Tests promotions date filter"""

    timestamp = datetime.now()

    date_filtered = swell.promotions.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-list-promotions-with-limit.yml')
def test_list_promotions_with_return_limit(swell):
    """Tests list promotions return limit"""

    limit = 1
    response = swell.promotions.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/promotions/test-promotions-expansion.yml')
def test_list_promotions_expansion(swell):
    """Tests promotions expansion param is correctly sent"""

    response = swell.promotions.list({"expand": ["orders"]})
    orders = response['results'][0]['orders']

    assert isinstance(orders, dict)


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-get-promotion.yml')
def test_get_promotion_by_id(swell, promotion_keys):
    """Tests get promotion by id"""

    response = swell.promotions.list()
    first_promotion_id = response['results'][0]['id']
    
    id_response = swell.promotions.get(first_promotion_id)

    assert set(promotion_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_promotion(swell):
    """Test fails with incorrect id type during get promotion"""

    with pytest.raises(TypeError):
        swell.promotions.get(123)


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-get-promotion-expanded.yml')
def test_get_promotion_expanded(swell, promotion_keys):
    """Tests get promotion expanded"""

    response = swell.promotions.list()
    first_promotion_id = response['results'][0]['id']

    id_response = swell.promotions.get(first_promotion_id, { "expand": ['orders'] })

    assert set(promotion_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-create-promotion.yml')
def test_create_promotion(swell, promotion_keys):
    """Tests create new promotion"""

    new_promotion = {
        'name': '90% Off Sale',
        'active': False,
        'discounts': {
            'value_type': 'percent',
            'value_percent': 90
        }
    }

    response = swell.promotions.create(new_promotion)

    assert set(promotion_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['name'] == new_promotion['name']


def test_fails_with_no_name(swell):
    """Tests fail when no name is provided"""

    with pytest.raises(ValueError):
        swell.promotions.create({
            'discounts': {
                'value_type': 'percent',
                'value_percent': 90
            },
        })

def test_fails_with_no_discounts(swell):
    """Tests fail when no discounts are provided"""

    with pytest.raises(ValueError):
        swell.promotions.create({
            'name': 'test'
        })


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-update-promotion.yml')
def test_update_promotion(swell, promotion_keys):
    """Tests updating a promotion"""

    response = swell.promotions.list()
    first_promotion_id = response['results'][0]['id']
    
    updates = {
        "id": first_promotion_id,
        "name": "new promotion name"
    }

    update_response = swell.promotions.update(updates)
    assert set(promotion_keys).issubset(update_response.keys())
    assert update_response["name"] == updates["name"]


def test_fails_with_no_id_update_promotion(swell):
    """Tests fails with missing id during promotion update"""

    with pytest.raises(Exception):
        swell.promotions.update({ "promotion1": "123 test" })


def test_fails_with_incorrect_id_update_promotion(swell):
    """Tests fails with incorrect id type during promotion update"""

    with pytest.raises(TypeError):
        swell.promotions.update({ "id": 123, "promotion1": "123 test"})


@vcr.use_cassette('tests/vcr_cassettes/promotions/test-delete-promotion.yml')
def test_delete_promotion(swell, promotion_keys):
    """Tests deleting a promotion"""

    response = swell.promotions.list()
    first_promotion_id = response['results'][0]['id']

    assert isinstance(first_promotion_id, str)
    
    delete_response = swell.promotions.delete(first_promotion_id)
    assert set(promotion_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_promotion(swell):
    """Test fails when no id provided to delete a promotion"""

    with pytest.raises(ValueError):
        swell.promotions.delete()


def test_failed_with_incorrect_id_type_delete_promotion(swell):
    """Test fails when incorrect id type provided to delete a promotion"""

    with pytest.raises(TypeError):
        swell.promotions.delete(123)
