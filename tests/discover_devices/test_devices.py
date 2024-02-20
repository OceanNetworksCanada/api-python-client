import pytest
import requests


def test_invalid_time_range_greater_start_time(requester):
    params_invalid_time_range_greater_start_time = {
        "deviceCode": "BPR-Folger-59",
        "dateFrom": "2020-01-01",
        "dateTo": "2019-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 23"):
        requester.getDevices(params_invalid_time_range_greater_start_time)


def test_invalid_time_range_future_start_time(requester):
    params_invalid_time_range_future_start_time = {
        "deviceCode": "BPR-Folger-59",
        "dateFrom": "2050-01-01",
    }
    with pytest.raises(requests.HTTPError, match=r"API Error 25"):
        requester.getDevices(params_invalid_time_range_future_start_time)


def test_invalid_param_value(requester):
    params_invalid_param_value = {"deviceCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDevices(params_invalid_param_value)


def test_invalid_param_name(requester):
    params_invalid_param_name = {"deviceCodes": "BPR-Folger-59"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getDevices(params_invalid_param_name)


def test_no_data(requester):
    params_no_data = {"deviceCode": "BPR-Folger-59", "dateTo": "1900-01-01"}
    with pytest.raises(requests.HTTPError, match=r"404 Client Error"):
        requester.getDevices(params_no_data)


def test_valid_params(requester, util):
    params = {
        "deviceCode": "BPR-Folger-59",
        "dateFrom": "2005-09-17",
        "dateTo": "2020-09-17",
    }
    expected_keys = {
        "cvTerm": dict,
        "dataRating": list,
        "deviceCategoryCode": str,
        "deviceCode": str,
        "deviceId": int,
        "deviceLink": str,
        "deviceName": str,
        "hasDeviceData": bool,
    }
    expected_keys_cv_term_device = {
        "uri": str,
        "vocabulary": str,
    }
    expected_keys_data_rating = {
        "dateFrom": str,
        "dateTo": None,
        "samplePeriod": float,
        "sampleSize": int,
    }
    data = requester.getDevices(params)

    assert len(data) > 0, "Valid devices test should return at least 1 row."

    util.assert_dict_key_types(data[0], expected_keys)
    util.assert_dict_key_types(
        data[0]["cvTerm"]["device"][0], expected_keys_cv_term_device
    )
    util.assert_dict_key_types(data[0]["dataRating"][0], expected_keys_data_rating)
