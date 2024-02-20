import pytest
import requests


def test_invalid_param_value(requester):
    params_invalid_param_value = {"deviceCategoryCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDeviceCategories(params_invalid_param_value)


def test_invalid_param_name(requester):
    params_invalid_param_name = {"deviceCategoryCodes": "CTD"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getDeviceCategories(params_invalid_param_name)


def test_no_data(requester):
    params_no_data = {
        "deviceCategoryCode": "CTD",
        "deviceCategoryName": "Conductivity",
        "description": "TemperatureXXX",
    }
    with pytest.raises(requests.HTTPError, match=r"404 Client Error"):
        requester.getDeviceCategories(params_no_data)


def test_valid_params(requester, util):
    params = {
        "deviceCategoryCode": "CTD",
        "deviceCategoryName": "Conductivity",
        "description": "Temperature",
    }
    expected_keys = {
        "cvTerm": dict,
        "description": str,
        "deviceCategoryCode": str,
        "deviceCategoryName": str,
        "hasDeviceData": bool,
        "longDescription": str,
    }

    expected_keys_cv_term_device_category = {
        "uri": str,
        "vocabulary": str,
    }

    data = requester.getDeviceCategories(params)

    assert len(data) > 0, "Valid device categories test should return at least 1 row."

    util.assert_dict_key_types(data[0], expected_keys)
    util.assert_dict_key_types(
        data[0]["cvTerm"]["deviceCategory"][0], expected_keys_cv_term_device_category
    )
