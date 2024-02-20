import pytest
import requests


def test_invalid_param_value(requester, params_location):
    params_invalid_param_value = params_location | {"locationCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getListByLocation(params_invalid_param_value)


def test_invalid_params_missing_required(requester, params_location):
    del params_location["locationCode"]
    with pytest.raises(requests.HTTPError, match=r"API Error 128"):
        requester.getListByLocation(params_location)


def test_invalid_param_name(requester, params_location):
    params_invalid_param_name = params_location | {"locationCodes": "NCBC"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getListByLocation(params_invalid_param_name)


def test_no_data(requester, params_location):
    params_no_data = params_location | {
        "dateFrom": "2000-01-01",
        "dateTo": "2000-01-02",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getListByLocation(params_no_data)


def test_valid_params_one_page(
    requester, params_location, params_location_multiple_pages
):
    data = requester.getListByLocation(params_location)
    data_all_pages = requester.getListByLocation(
        params_location_multiple_pages, allPages=True
    )

    assert (
        len(data["files"]) > params_location_multiple_pages["rowLimit"]
    ), "Test should return at least `rowLimit` rows."

    assert data["next"] is None, "Test should return only one page."

    assert (
        data_all_pages["files"] == data["files"]
    ), "Test should concatenate rows for all pages."

    assert data_all_pages["next"] is None, "Test should return only one page."


def test_valid_params_multiple_pages(requester, params_location_multiple_pages):
    data = requester.getListByLocation(params_location_multiple_pages)

    assert (
        len(data["files"]) == params_location_multiple_pages["rowLimit"]
    ), "Test should only return `rowLimit` rows."

    assert data["next"] is not None, "Test should return multiple pages."
