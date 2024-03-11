import pytest
import requests


def test_invalid_time_range_greater_start_time(requester):
    params_invalid_time_range_greater_start_time = {
        "locationCode": "BACAX",
        "deviceCategoryCode": "CTD",
        "dateFrom": "2020-01-01",
        "dateTo": "2019-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 23"):
        requester.getDeployments(params_invalid_time_range_greater_start_time)


def test_invalid_time_range_future_start_time(requester):
    params_invalid_time_range_future_start_time = {
        "locationCode": "BACAX",
        "deviceCategoryCode": "CTD",
        "dateFrom": "2050-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 25"):
        requester.getDeployments(params_invalid_time_range_future_start_time)


def test_invalid_param_value(requester):
    params_invalid_param_value = {"locationCode": "XYZ123", "deviceCategoryCode": "CTD"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDeployments(params_invalid_param_value)


def test_invalid_param_name(requester):
    params_invalid_param_name = {"locationCodes": "BACAX", "deviceCategoryCode": "CTD"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getDeployments(params_invalid_param_name)


def test_no_data(requester):
    params_no_data = {
        "locationCode": "BACAX",
        "deviceCategoryCode": "CTD",
        "dateTo": "1900-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDeployments(params_no_data)


def test_valid_params(requester, util):
    params = {
        "locationCode": "BACAX",
        "deviceCategoryCode": "CTD",
        "dateFrom": "2015-09-17",
        "dateTo": "2015-09-17T13:00:00.000Z",
    }
    expected_keys = {
        "begin": str,
        "citation": dict,
        "depth": float,
        "deviceCategoryCode": str,
        "deviceCode": str,
        "end": str,
        "hasDeviceData": bool,
        "heading": None,
        "lat": float,
        "locationCode": str,
        "lon": float,
        "pitch": None,
        "roll": None,
    }

    expected_keys_citation = {
        "citation": str,
        "doi": str,
        "landingPageUrl": str,
        "queryPid": None,
    }

    data = requester.getDeployments(params)

    assert len(data) > 0, "Valid deployment test should return at least 1 row."

    util.assert_dict_key_types(data[0], expected_keys)
    util.assert_dict_key_types(data[0]["citation"], expected_keys_citation)
