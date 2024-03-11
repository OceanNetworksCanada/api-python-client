import pytest
import requests


def test_invalid_time_range_greater_start_time(requester):
    params_invalid_time_range_greater_start_time = {
        "locationCode": "FGPD",
        "dateFrom": "2020-01-01",
        "dateTo": "2019-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 23"):
        requester.getLocations(params_invalid_time_range_greater_start_time)


def test_invalid_time_range_future_start_time(requester):
    params_invalid_time_range_future_start_time = {
        "locationCode": "FGPD",
        "dateFrom": "2050-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 25"):
        requester.getLocations(params_invalid_time_range_future_start_time)


def test_invalid_param_value(requester):
    params_invalid_param_value = {"locationCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getLocations(params_invalid_param_value)


def test_invalid_param_name(requester):
    params_invalid_param_name = {"locationCodes": "FGPD"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getLocations(params_invalid_param_name)


def test_no_data(requester):
    params_no_data = {"locationCode": "FGPD", "dateTo": "1900-01-01"}
    with pytest.raises(requests.HTTPError, match=r"404 Client Error"):
        requester.getLocations(params_no_data)


def test_valid_params(requester, util):
    params = {
        "locationCode": "FGPD",
        "dateFrom": "2005-09-17",
        "dateTo": "2020-09-17",
    }
    expected_keys = {
        "deployments": int,
        "locationName": str,
        "depth": float,
        "bbox": dict,
        "description": str,
        "hasDeviceData": bool,
        "lon": float,
        "locationCode": str,
        "hasPropertyData": bool,
        "lat": float,
        "dataSearchURL": str,
    }
    expected_keys_bbox = {
        "maxDepth": float,
        "maxLat": float,
        "maxLon": float,
        "minDepth": float,
        "minLat": float,
        "minLon": float,
    }
    data = requester.getLocations(params)

    assert len(data) > 0, "Valid locations test should return at least 1 row."

    util.assert_dict_key_types(data[0], expected_keys)
    util.assert_dict_key_types(data[0]["bbox"], expected_keys_bbox)
