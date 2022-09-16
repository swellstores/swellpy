import vcr
import pytest
from datetime import datetime

@pytest.fixture
def credit_keys():
    yield ['id', 'parent_id', 'amount']


@vcr.use_cassette('tests/vcr_cassettes/credits/test-list-credits.yml')
def test_list_credits(swell):
    """Tests list all credits"""

    response = swell.accounts.credits.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/credits/test-credits-date-filter.yml')
def test_list_credits_date_filter(swell):
    """Tests credits date filter"""

    timestamp = datetime.now()

    date_filtered = swell.accounts.credits.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/credits/test-list-credits-with-limit.yml')
def test_list_credits_with_return_limit(swell):
    """Tests list credits return limit"""

    limit = 1
    response = swell.accounts.credits.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit



@vcr.use_cassette('tests/vcr_cassettes/credits/test-credits-expansion.yml')
def test_list_credits_expansion(swell):
    """Tests credits expansion param is correctly sent"""

    response = swell.accounts.credits.list({"expand": ["parent"]})
    parent = response['results'][0]['parent']

    assert isinstance(parent, dict)


@vcr.use_cassette('tests/vcr_cassettes/credits/test-get-credits.yml')
def test_get_credits_by_id(swell, credit_keys):
    """Tests get credits by id"""

    response = swell.accounts.credits.list()
    first_account_id = response['results'][0]['id']
    
    id_response = swell.accounts.credits.get(first_account_id)

    assert set(credit_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_account_credits(swell):
    """Test fails with incorrect id type during get account credits"""

    with pytest.raises(TypeError):
        swell.accounts.credits.get(123)


@vcr.use_cassette('tests/vcr_cassettes/credits/test-get-credits-expanded.yml')
def test_get_account_credits_expanded(swell, credit_keys):
    """Tests get account credits expanded"""

    response = swell.accounts.credits.list()
    first_account_id = response['results'][0]['id']
    credit_keys.append('parent')

    id_response = swell.accounts.credits.get(first_account_id, { "expand": ['parent'] })

    assert set(credit_keys).issubset(id_response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/credits/test-create-account-credit.yml')
def test_create_account_credit(swell, credit_keys):
    """Tests create new account credit"""

    response = swell.accounts.list()
    first_account_id = response['results'][0]['id']
    
    new_account_credit = {
        'parent_id': first_account_id,
        'amount': 10
    }

    response = swell.accounts.credits.create(new_account_credit)

    assert set(credit_keys).issubset(response.keys()), "All keys should be in the response"
    assert isinstance(response['id'], str)
    assert response['amount'] == new_account_credit['amount']


def test_fails_with_no_id(swell):
    """Tests fail when no parent id is provided"""

    with pytest.raises(ValueError):
        swell.accounts.credits.create({"amount": 10})

def test_fails_with_no_credit1(swell):
    """Tests fail when no amount is provided"""

    with pytest.raises(ValueError):
        swell.accounts.credits.create({"parent_id": "123"})



@vcr.use_cassette('tests/vcr_cassettes/credits/test-update-account-credit.yml')
def test_update_account_credit(swell, credit_keys):
    """Tests updating an account credit"""

    response = swell.accounts.credits.list()
    first_account_credit_id = response['results'][0]['id']
    
    updates = {
        "id": first_account_credit_id,
        "reason": "refund"
    }

    update_response = swell.accounts.credits.update(updates)
    assert set(credit_keys).issubset(update_response.keys())
    assert update_response["reason"] == updates["reason"]


def test_fails_with_no_id_update_account_credit(swell):
    """Tests fails with missing id during account credit update"""

    with pytest.raises(Exception):
        swell.accounts.credits.update({ "reason": "refund" })


def test_fails_with_incorrect_id_update_account_credit(swell):
    """Tests fails with incorrect id type during account credit update"""

    with pytest.raises(TypeError):
        swell.accounts.credits.update({ "id": 123, "reason": "refund"})


@vcr.use_cassette('tests/vcr_cassettes/credits/test-delete-account-credit.yml')
def test_delete_account(swell, credit_keys):
    """Tests deleting an account credit"""

    response = swell.accounts.credits.list()
    first_account_credit_id = response['results'][0]['id']

    assert isinstance(first_account_credit_id, str)
    
    delete_response = swell.accounts.credits.delete(first_account_credit_id)
    assert set(credit_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_account_credit(swell):
    """Test fails when no id provided to delete a account credit"""

    with pytest.raises(Exception):
        swell.accounts.credits.delete(123)


def test_failed_with_incorrect_id_type_delete_account_credit(swell):
    """Test fails when incorrect id type provided to delete an account credit"""

    with pytest.raises(TypeError):
        swell.accounts.credits.delete(123)
