import vcr
import pytest
from datetime import datetime

@pytest.fixture
def use_keys():
    yield ['id', 'parent_id', 'amount']


@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-list-debits.yml')
def test_list_debits(swell):
    """Tests list all debits"""

    response = swell.giftcards.debits.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-debits-date-filter.yml')
def test_list_debits_date_filter(swell):
    """Tests debits date filter"""

    timestamp = datetime.now()

    date_filtered = swell.giftcards.debits.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-list-debits-with-limit.yml')
def test_list_debits_with_return_limit(swell):
    """Tests list debits return limit"""

    limit = 1
    response = swell.giftcards.debits.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-debits-expansion.yml')
def test_list_debits_expansion(swell):
    """Tests debits expansion param is correctly sent"""

    response = swell.giftcards.debits.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-get-debits.yml')
def test_get_debits_by_giftcard_id(swell, use_keys):
    """Tests get debits by giftcard id"""

    response = swell.giftcards.debits.list()
    first_giftcard_id = response['results'][0]['id']
    
    id_response = swell.giftcards.debits.get(first_giftcard_id)

    assert set(use_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_giftcard_debits(swell):
    """Test fails with incorrect id type during get giftcard debits"""

    with pytest.raises(TypeError):
        swell.giftcards.debits.get(123)


@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-get-debits-expanded.yml')
def test_get_giftcard_debits_expanded(swell, use_keys):
    """Tests get giftcard debits expanded"""

    response = swell.giftcards.debits.list()
    first_giftcard_id = response['results'][0]['id']
    use_keys.append('parent')

    id_response = swell.giftcards.debits.get(first_giftcard_id, { "expand": ['parent'] })

    assert set(use_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-create-giftcard-use.yml')
def test_create_giftcard_use(swell, use_keys):
    """Tests create new giftcard use"""

    response = swell.giftcards.list({ 'expand': 'codes'})
    first_giftcard = response['results'][0]
    
    new_giftcard_use = {
        'parent_id': first_giftcard['id'],
        'amount': 1

    }

    response = swell.giftcards.debits.create(new_giftcard_use)

    assert set(use_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['parent_id'] == new_giftcard_use['parent_id']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.giftcards.debits.create({'amount': 50})

def test_fails_with_no_amount(swell):
    """Tests fail when no amount is provided"""

    with pytest.raises(ValueError):
        swell.giftcards.debits.create({'parent_id': '123'})


@vcr.use_cassette('tests/vcr_cassettes/giftcard-debits/test-delete-giftcard-use.yml')
def test_delete_giftcard_use(swell, use_keys):
    """Tests deleting an giftcard use"""

    response = swell.giftcards.debits.list()
    first_giftcard_use_id = response['results'][0]['id']

    assert isinstance(first_giftcard_use_id, str)
    
    delete_response = swell.giftcards.debits.delete(first_giftcard_use_id)
    assert set(use_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_giftcard_use(swell):
    """Test fails when no id provided to delete a giftcard use"""

    with pytest.raises(Exception):
        swell.giftcards.debits.delete(123)


def test_failed_with_incorrect_id_type_delete_giftcard_use(swell):
    """Test fails when incorrect id type provided to delete an giftcard use"""

    with pytest.raises(TypeError):
        swell.giftcards.debits.delete(123)
