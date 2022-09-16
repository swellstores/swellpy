import vcr
import pytest
from datetime import datetime

@pytest.fixture
def category_keys():
    yield ['id', 'name']


@vcr.use_cassette('tests/vcr_cassettes/categories/test-list-categories.yml')
def test_list_categories(swell):
    """Tests list all categories"""

    response = swell.categories.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/categories/test-categories-date-filter.yml')
def test_list_categories_date_filter(swell):
    """Tests categories date filter"""

    timestamp = datetime.now()

    date_filtered = swell.categories.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/categories/test-list-categories-with-limit.yml')
def test_list_categories_with_return_limit(swell):
    """Tests list categories return limit"""

    limit = 1
    response = swell.categories.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/categories/test-get-category.yml')
def test_get_category_by_id(swell, category_keys):
    """Tests get category by id"""

    response = swell.categories.list()
    first_category_id = response['results'][0]['id']
    
    id_response = swell.categories.get(first_category_id)

    assert set(category_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_category(swell):
    """Test fails with incorrect id type during get category"""

    with pytest.raises(TypeError):
        swell.categories.get(123)


@vcr.use_cassette('tests/vcr_cassettes/categories/test-create-category.yml')
def test_create_category(swell, category_keys):
    """Tests create new category"""

    new_category = {
        'name': 'New Category',
    }

    response = swell.categories.create(new_category)

    assert set(category_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['name'] == new_category['name']


def test_fails_with_no_amount(swell):
    """Tests fail when no name is provided"""

    with pytest.raises(ValueError):
        swell.categories.create({})


@vcr.use_cassette('tests/vcr_cassettes/categories/test-update-category.yml')
def test_update_category(swell, category_keys):
    """Tests updating a category"""

    response = swell.categories.list()
    first_category_id = response['results'][0]['id']
    
    updates = {
        "id": first_category_id,
        "name": 'new name 2'
    }

    update_response = swell.categories.update(updates)
    assert set(category_keys).issubset(update_response.keys())
    assert update_response["name"] == updates["name"]


def test_fails_with_no_id_update_category(swell):
    """Tests fails with missing id during category update"""

    with pytest.raises(Exception):
        swell.categories.update({ "name": 'new name' })


def test_fails_with_incorrect_id_update_category(swell):
    """Tests fails with incorrect id type during category update"""

    with pytest.raises(TypeError):
        swell.categories.update({ "id": 123, "name": 'new name'})


@vcr.use_cassette('tests/vcr_cassettes/categories/test-delete-category.yml')
def test_delete_category(swell, category_keys):
    """Tests deleting a category"""

    response = swell.categories.list()
    first_category_id = response['results'][0]['id']

    assert isinstance(first_category_id, str)
    
    delete_response = swell.categories.delete(first_category_id)
    assert set(category_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_category(swell):
    """Test fails when no id provided to delete a category"""

    with pytest.raises(ValueError):
        swell.categories.delete()


def test_failed_with_incorrect_id_type_delete_category(swell):
    """Test fails when incorrect id type provided to delete a category"""

    with pytest.raises(TypeError):
        swell.categories.delete(123)
