import vcr
import pytest
from datetime import datetime

@pytest.fixture
def generation_keys():
    yield ['id', 'parent_id', 'count']


@vcr.use_cassette('tests/vcr_cassettes/generations/test-list-generations.yml')
def test_list_generations(swell):
    """Tests list all generations"""

    response = swell.coupon_generations.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/generations/test-generations-date-filter.yml')
def test_list_generations_date_filter(swell):
    """Tests generations date filter"""

    timestamp = datetime.now()

    date_filtered = swell.coupon_generations.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/generations/test-list-generations-with-limit.yml')
def test_list_generations_with_return_limit(swell):
    """Tests list generations return limit"""

    limit = 1
    response = swell.coupon_generations.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/generations/test-generations-expansion.yml')
def test_list_generations_expansion(swell):
    """Tests generations expansion param is correctly sent"""

    response = swell.coupon_generations.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/generations/test-get-generations.yml')
def test_get_generations_by_coupon_id(swell, generation_keys):
    """Tests get generations by coupon id"""

    response = swell.coupon_generations.list()
    first_coupon_id = response['results'][0]['id']
    
    id_response = swell.coupon_generations.get(first_coupon_id)

    assert set(generation_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_coupon_generations(swell):
    """Test fails with incorrect id type during get coupon generations"""

    with pytest.raises(TypeError):
        swell.coupon_generations.get(123)


@vcr.use_cassette('tests/vcr_cassettes/generations/test-get-generations-expanded.yml')
def test_get_coupon_generations_expanded(swell, generation_keys):
    """Tests get coupon generations expanded"""

    response = swell.coupon_generations.list()
    first_coupon_id = response['results'][0]['id']
    generation_keys.append('parent')

    id_response = swell.coupon_generations.get(first_coupon_id, { "expand": ['parent'] })

    assert set(generation_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/generations/test-create-coupon-generation.yml')
def test_create_coupon_generation(swell, generation_keys):
    """Tests create new coupon generation"""

    response = swell.coupon_generations.list()
    first_coupon_id = response['results'][0]['id']
    
    new_coupon_generation = {
        'parent_id': first_coupon_id,
        'count': 50
    }

    response = swell.coupon_generations.create(new_coupon_generation)

    assert set(generation_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['count'] == new_coupon_generation['count']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.coupon_generations.create({"count": 100})

def test_fails_with_no_count(swell):
    """Tests fail when no count is provided"""

    with pytest.raises(ValueError):
        swell.coupon_generations.create({"parent_id": "123"})



# @vcr.use_cassette('tests/vcr_cassettes/generations/test-update-coupon-generation.yml')
# def test_update_coupon_generation(swell, generation_keys):
#     """Tests updating an coupon generation"""

#     response = swell.coupon_generations.list()
#     first_coupon_generation_id = response['results'][0]['id']
    
#     updates = {
#         "id": first_coupon_generation_id,
#         "count": 25
#     }

#     update_response = swell.coupon_generations.update(updates)
#     assert set(generation_keys).issubset(update_response.keys())
#     assert update_response["count"] == updates["count"]


def test_fails_with_no_id_update_coupon_generation(swell):
    """Tests fails with missing id during coupon generation update"""

    with pytest.raises(Exception):
        swell.coupon_generations.update({ "count": 50 })


def test_fails_with_incorrect_id_update_coupon_generation(swell):
    """Tests fails with incorrect id type during coupon generation update"""

    with pytest.raises(TypeError):
        swell.coupon_generations.update({ "id": 123, "count": 50})


@vcr.use_cassette('tests/vcr_cassettes/generations/test-delete-coupon-generation.yml')
def test_delete_coupon_generation(swell, generation_keys):
    """Tests deleting an coupon generation"""

    response = swell.coupon_generations.list()
    first_coupon_generation_id = response['results'][0]['id']

    assert isinstance(first_coupon_generation_id, str)
    
    delete_response = swell.coupon_generations.delete(first_coupon_generation_id)
    assert set(generation_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_coupon_generation(swell):
    """Test fails when no id provided to delete a coupon generation"""

    with pytest.raises(Exception):
        swell.coupon_generations.delete(123)


def test_failed_with_incorrect_id_type_delete_coupon_generation(swell):
    """Test fails when incorrect id type provided to delete an coupon generation"""

    with pytest.raises(TypeError):
        swell.coupon_generations.delete(123)
