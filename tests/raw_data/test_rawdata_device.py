import pytest
import requests


@pytest.fixture
def params():
    return {
        "deviceCode": "BPR-Folger-59",
        "dateFrom": "2019-11-23T00:00:00.000Z",
        "dateTo": "2019-11-23T00:01:00.000Z",
        "rowLimit": 80000,
    }


@pytest.fixture
def params_multiple_pages(params):
    # rowLimit should be less than the total number of rows.
    return params | {"rowLimit": 25}


def test_invalid_param_value(requester, params):
    params_invalid_param_value = params | {"deviceCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getRawdata(params_invalid_param_value)


def test_invalid_param_name(requester, params):
    params_invalid_param_name = params | {"deviceCodes": "BPR-Folger-59"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getRawdata(params_invalid_param_name)


def test_no_data(requester, params):
    params_no_data = params | {"dateFrom": "2000-01-01", "dateTo": "2000-01-02"}
    data = requester.getRawdata(params_no_data)

    assert _get_row_num(data) == 0


def test_different_date_format_all_pages(requester, params_multiple_pages):
    params_different_date_format = params_multiple_pages | {
        "dateFrom": "2019-11-23T23:59:00.000Z",
        "dateTo": "2019-11-24",
    }
    requester.getRawdata(params_different_date_format, allPages=True)


def test_valid_params_one_page(requester, params, params_multiple_pages):
    data = requester.getRawdata(params)
    data_all_pages = requester.getRawdata(params_multiple_pages, allPages=True)

    assert (
        _get_row_num(data) > params_multiple_pages["rowLimit"]
    ), "Test should return at least `rowLimit` rows for each sensor."

    assert data["next"] is None, "Test should return only one page."

    assert (
        data_all_pages["data"] == data["data"]
    ), "Test should concatenate rows for all pages."

    assert data_all_pages["next"] is None, "Test should return only one page."


def test_valid_params_multi_pages(requester, params_multiple_pages):
    data = requester.getRawdata(params_multiple_pages)

    assert (
        _get_row_num(data) == params_multiple_pages["rowLimit"]
    ), "Test should only return `rowLimit` rows for each sensor."

    assert data["next"] is not None, "Test should return multiple pages."


def _get_row_num(data):
    return len(data["data"]["readings"])
