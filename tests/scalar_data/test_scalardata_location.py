import pytest
import requests


@pytest.fixture
def params_multiple_pages(params_location):
    # rowLimit should be less than the total number of rows.
    return params_location | {"rowLimit": 25}


def test_invalid_param_value(requester, params_location):
    params_invalid_param_value = params_location | {"locationCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDirectByLocation(params_invalid_param_value)


def test_invalid_param_name(requester, params_location):
    params_invalid_param_name = params_location | {"locationCodes": "NCBC"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getDirectByLocation(params_invalid_param_name)


def test_no_data(requester, params_location):
    params_no_data = params_location | {
        "dateFrom": "2000-01-01",
        "dateTo": "2000-01-02",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDirectByLocation(params_no_data)


def test_valid_params_one_page(requester, params_location, params_multiple_pages):
    data = requester.getDirectByLocation(params_location)
    data_all_pages = requester.getDirectByLocation(params_multiple_pages, allPages=True)

    assert (
        _get_row_num(data) > params_multiple_pages["rowLimit"]
    ), "Test should return at least `rowLimit` rows for each sensor."

    assert data["next"] is None, "Test should return only one page."

    assert (
        data_all_pages["sensorData"][0]["data"] == data["sensorData"][0]["data"]
    ), "Test should concatenate rows for all pages."

    assert data_all_pages["next"] is None, "Test should return only one page."


def test_valid_params_multiple_pages(requester, params_multiple_pages):
    data = requester.getDirectByLocation(params_multiple_pages)

    assert (
        _get_row_num(data) == params_multiple_pages["rowLimit"]
    ), "Test should only return `rowLimit` rows for each sensor."

    assert data["next"] is not None, "Test should return multiple pages."


def _get_row_num(data):
    return len(data["sensorData"][0]["data"]["values"])
