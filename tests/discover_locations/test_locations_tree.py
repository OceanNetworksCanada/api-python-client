import pytest
import requests


def test_invalid_time_range_greater_start_time(requester):
    params_invalid_time_range_greater_start_time = {
        "locationCode": "ARCT",
        "dateFrom": "2020-01-01",
        "dateTo": "2019-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 23"):
        requester.getLocationHierarchy(params_invalid_time_range_greater_start_time)


def test_invalid_time_range_future_start_time(requester):
    params_invalid_time_range_future_start_time = {
        "locationCode": "ARCT",
        "dateFrom": "2050-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 25"):
        requester.getLocationHierarchy(params_invalid_time_range_future_start_time)


def test_invalid_param_value(requester):
    params_invalid_param_value = {"locationCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getLocationHierarchy(params_invalid_param_value)


def test_invalid_param(requester):
    params_invalid_param_name = {"locationCodes": "ARCT"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getLocationHierarchy(params_invalid_param_name)


def test_no_data(requester):
    params_no_data = {"locationCode": "ARCT", "dateTo": "1900-01-01"}
    with pytest.raises(requests.HTTPError, match=r"404 Client Error"):
        requester.getLocationHierarchy(params_no_data)


def test_valid_params(requester, util):
    params = {"locationCode": "ARCT", "deviceCategoryCode": "VIDEOCAM"}
    expected_keys = {
        "locationName": str,
        "children": list,
        "description": str,
        "hasDeviceData": bool,
        "locationCode": str,
        "hasPropertyData": bool,
    }

    data = requester.getLocationHierarchy(params)

    assert len(data) > 0, "Valid locations tree test should return at least 1 row."

    assert (
        len(data[0]["children"]) > 0
    ), "valid locations tree test should return at least 1 row in the children."

    util.assert_dict_key_types(data[0], expected_keys)
