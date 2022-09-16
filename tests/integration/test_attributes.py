import vcr
import pytest
from datetime import datetime

@pytest.fixture
def attribute_keys():
    yield ['id', 'name']


@vcr.use_cassette('tests/vcr_cassettes/attributes/test-list-attributes.yml')
def test_list_attributes(swell):
    """Tests list all attributes"""

    response = swell.attributes.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/attributes/test-attributes-date-filter.yml')
def test_list_attributes_date_filter(swell):
    """Tests attributes date filter"""

    timestamp = datetime.now()

    date_filtered = swell.attributes.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/attributes/test-list-attributes-with-limit.yml')
def test_list_attributes_with_return_limit(swell):
    """Tests list attributes return limit"""

    limit = 1
    response = swell.attributes.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/attributes/test-get-attribute.yml')
def test_get_attribute_by_id(swell, attribute_keys):
    """Tests get attribute by id"""

    response = swell.attributes.list()
    first_attribute_id = response['results'][0]['id']
    
    id_response = swell.attributes.get(first_attribute_id)

    assert set(attribute_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_attribute(swell):
    """Test fails with incorrect id type during get attribute"""

    with pytest.raises(TypeError):
        swell.attributes.get(123)


@vcr.use_cassette('tests/vcr_cassettes/attributes/test-create-attribute.yml')
def test_create_attribute(swell, attribute_keys):
    """Tests create new attribute"""

    new_attribute = {
        'name': 'Test Material',
        "type": "dropdown",
        "values": [
            "Cotton",
            "Polyester",
            "Wool"
        ]
    }

    response = swell.attributes.create(new_attribute)

    assert set(attribute_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['values'] == new_attribute['values']


def test_fails_with_no_amount(swell):
    """Tests fail when no name is provided"""

    with pytest.raises(ValueError):
        swell.attributes.create({})


@vcr.use_cassette('tests/vcr_cassettes/attributes/test-update-attribute.yml')
def test_update_attribute(swell, attribute_keys):
    """Tests updating a attribute"""

    response = swell.attributes.list()
    first_attribute_id = response['results'][0]['id']
    
    updates = {
        "id": first_attribute_id,
        "name": 'new name 2'
    }

    update_response = swell.attributes.update(updates)
    assert set(attribute_keys).issubset(update_response.keys())
    assert update_response["name"] == updates["name"]


def test_fails_with_no_id_update_attribute(swell):
    """Tests fails with missing id during attribute update"""

    with pytest.raises(Exception):
        swell.attributes.update({ "name": 'new name' })


def test_fails_with_incorrect_id_update_attribute(swell):
    """Tests fails with incorrect id type during attribute update"""

    with pytest.raises(TypeError):
        swell.attributes.update({ "id": 123, "name": 'new name'})


@vcr.use_cassette('tests/vcr_cassettes/attributes/test-delete-attribute.yml')
def test_delete_attribute(swell, attribute_keys):
    """Tests deleting a attribute"""

    response = swell.attributes.list()
    first_attribute_id = response['results'][0]['id']

    assert isinstance(first_attribute_id, str)
    
    delete_response = swell.attributes.delete(first_attribute_id)
    assert set(attribute_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_attribute(swell):
    """Test fails when no id provided to delete a attribute"""

    with pytest.raises(ValueError):
        swell.attributes.delete()


def test_failed_with_incorrect_id_type_delete_attribute(swell):
    """Test fails when incorrect id type provided to delete a attribute"""

    with pytest.raises(TypeError):
        swell.attributes.delete(123)
