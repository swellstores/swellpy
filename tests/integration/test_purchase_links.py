import vcr
import pytest
from datetime import datetime

@pytest.fixture
def purchase_link_keys():
    yield ['id', 'name']


@vcr.use_cassette('tests/vcr_cassettes/purchase_links/test-list-purchase-links.yml')
def test_list_purchase_links(swell):
    """Tests list all purchase links"""

    response = swell.purchase_links.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/purchase_links/test-purchase-links-date-filter.yml')
def test_list_purchase_links_date_filter(swell):
    """Tests purchase links date filter"""

    timestamp = datetime.now()

    date_filtered = swell.purchase_links.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/purchase_links/test-list-purchase-links-with-limit.yml')
def test_list_purchase_links_with_return_limit(swell):
    """Tests list purchase links return limit"""

    limit = 1
    response = swell.purchase_links.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/purchase_links/test-get-purchase-link.yml')
def test_get_purchase_link_by_id(swell, purchase_link_keys):
    """Tests get purchase link by id"""

    response = swell.purchase_links.list()
    first_purchase_link_id = response['results'][0]['id']
    
    id_response = swell.purchase_links.get(first_purchase_link_id)

    assert set(purchase_link_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_purchase_link(swell):
    """Test fails with incorrect id type during get purchase link"""

    with pytest.raises(TypeError):
        swell.purchase_links.get(123)


@vcr.use_cassette('tests/vcr_cassettes/purchase_links/test-create-purchase_link.yml')
def test_create_purchase_link(swell, purchase_link_keys):
    """Tests create new purchase_link"""

    new_purchase_link = {
        'name': 'New purchase link',
    }

    response = swell.purchase_links.create(new_purchase_link)

    assert set(purchase_link_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['name'] == new_purchase_link['name']


def test_fails_with_no_amount(swell):
    """Tests fail when no name is provided"""

    with pytest.raises(ValueError):
        swell.purchase_links.create({})


@vcr.use_cassette('tests/vcr_cassettes/purchase_links/test-update-purchase-link.yml')
def test_update_purchase_link(swell, purchase_link_keys):
    """Tests updating a purchase link"""

    response = swell.purchase_links.list()
    first_purchase_link_id = response['results'][0]['id']
    
    updates = {
        "id": first_purchase_link_id,
        "name": 'new name 2'
    }

    update_response = swell.purchase_links.update(updates)
    assert set(purchase_link_keys).issubset(update_response.keys())
    assert update_response["name"] == updates["name"]


def test_fails_with_no_id_update_purchase_link(swell):
    """Tests fails with missing id during purchase link update"""

    with pytest.raises(Exception):
        swell.purchase_links.update({ "name": 'new name' })


def test_fails_with_incorrect_id_update_purchase_link(swell):
    """Tests fails with incorrect id type during purchase link update"""

    with pytest.raises(TypeError):
        swell.purchase_links.update({ "id": 123, "name": 'new name'})


@vcr.use_cassette('tests/vcr_cassettes/purchase_links/test-delete-purchase-link.yml')
def test_delete_purchase_link(swell, purchase_link_keys):
    """Tests deleting a purchase link"""

    response = swell.purchase_links.list()
    first_purchase_link_id = response['results'][0]['id']

    assert isinstance(first_purchase_link_id, str)
    
    delete_response = swell.purchase_links.delete(first_purchase_link_id)
    assert set(purchase_link_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_purchase_link(swell):
    """Test fails when no id provided to delete a purchase link"""

    with pytest.raises(ValueError):
        swell.purchase_links.delete()


def test_failed_with_incorrect_id_type_delete_purchase_link(swell):
    """Test fails when incorrect id type provided to delete a purchase link"""

    with pytest.raises(TypeError):
        swell.purchase_links.delete(123)
