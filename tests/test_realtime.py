import pytest
import requests


@pytest.fixture
def no_data_filters():
    return {
        "locationCode": "CRIP.C1",
        "deviceCategoryCode": "CTD",
        "dateFrom": "2015-03-24T00:00:00.000Z",
        "dateTo": "2015-03-24T00:00:10.000Z",
    }


@pytest.fixture
def bad_data_filters(no_data_filters):
    return {**no_data_filters, "propertyCode": "BANANA"}


def test_no_data_filters(requester, no_data_filters):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getDirectByLocation(filters=no_data_filters)


def test_bad_filters(requester, bad_data_filters):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getDirectByLocation(filters=bad_data_filters)


def test_raw_no_data_filters(requester, no_data_filters):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getDirectRawByLocation(filters=no_data_filters)


def test_raw_bad_filters(requester, bad_data_filters):
    with pytest.raises(requests.HTTPError, match=r"Error 129"):
        requester.getDirectRawByLocation(filters=bad_data_filters)
