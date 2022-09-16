import vcr
import pytest
from datetime import datetime

@pytest.fixture
def invoice_keys():
    yield ['id', 'account_id', 'subscription_id']


@vcr.use_cassette('tests/vcr_cassettes/invoices/test-list-invoices.yml')
def test_list_invoices(swell):
    """Tests list all invoices"""

    response = swell.invoices.list()

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)


@vcr.use_cassette('tests/vcr_cassettes/invoices/test-invoices-date-filter.yml')
def test_list_invoices_date_filter(swell):
    """Tests invoices date filter"""

    timestamp = datetime.now()

    date_filtered = swell.invoices.list({
        "date_created": { "$gte": timestamp },
    })

    assert isinstance(date_filtered, dict)
    assert isinstance(date_filtered['results'], list)
    assert isinstance(date_filtered['count'], int)
    assert len(date_filtered['results']) == 0
    assert date_filtered['count'] == 0


@vcr.use_cassette('tests/vcr_cassettes/invoices/test-list-invoices-with-limit.yml')
def test_list_invoices_with_return_limit(swell):
    """Tests list invoices return limit"""

    limit = 1
    response = swell.invoices.list({"limit": limit})
    results_length = len(response['results'])

    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['count'], int)
    assert results_length <= limit


@vcr.use_cassette('tests/vcr_cassettes/invoices/test-get-invoice.yml')
def test_get_invoice_by_id(swell, invoice_keys):
    """Tests get invoice by id"""

    response = swell.invoices.list()
    first_invoice_id = response['results'][0]['id']
    
    id_response = swell.invoices.get(first_invoice_id)

    assert set(invoice_keys).issubset(id_response.keys()), "All keys should be in the response"


def test_fails_with_incorrect_id_get_invoice(swell):
    """Test fails with incorrect id type during get invoice"""

    with pytest.raises(TypeError):
        swell.invoices.get(123)




@vcr.use_cassette('tests/vcr_cassettes/invoices/test-update-invoice.yml')
def test_update_invoice(swell, invoice_keys):
    """Tests updating a invoice"""

    response = swell.invoices.list()
    first_invoice_id = response['results'][0]['id']
    
    updates = {
        "id": first_invoice_id,
        "amount": 99
    }

    update_response = swell.invoices.update(updates)
    assert set(invoice_keys).issubset(update_response.keys())
    assert update_response["amount"] == updates["amount"]


def test_fails_with_no_id_update_invoice(swell):
    """Tests fails with missing id during invoice update"""

    with pytest.raises(Exception):
        swell.invoices.update({ "amount": 50 })


def test_fails_with_incorrect_id_update_invoice(swell):
    """Tests fails with incorrect id type during invoice update"""

    with pytest.raises(TypeError):
        swell.invoices.update({ "id": 123, "amount": 90})


@vcr.use_cassette('tests/vcr_cassettes/invoices/test-delete-invoice.yml')
def test_delete_invoice(swell, invoice_keys):
    """Tests deleting a invoice"""

    response = swell.invoices.list()
    first_invoice_id = response['results'][0]['id']

    assert isinstance(first_invoice_id, str)
    
    delete_response = swell.invoices.delete(first_invoice_id)
    assert set(invoice_keys).issubset(delete_response.keys()), "All keys should be in the response"


def test_failed_with_no_id_delete_invoice(swell):
    """Test fails when no id provided to delete a invoice"""

    with pytest.raises(ValueError):
        swell.invoices.delete()


def test_failed_with_incorrect_id_type_delete_invoice(swell):
    """Test fails when incorrect id type provided to delete a invoice"""

    with pytest.raises(TypeError):
        swell.invoices.delete(123)
