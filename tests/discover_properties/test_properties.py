import pytest
import requests


def test_invalid_param_value(requester):
    params_invalid_param_value = {"propertyCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getProperties(params_invalid_param_value)


def test_invalid_param_name(requester):
    params_invalid_param_name = {"propertyCodes": "conductivity"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getProperties(params_invalid_param_name)


def test_no_data(requester):
    params_no_data = {
        "propertyCode": "conductivity",
        "locationCode": "SAAN",
    }

    with pytest.raises(requests.HTTPError, match=r"404 Client Error"):
        requester.getProperties(params_no_data)


def test_valid_params(requester, util):
    params = {
        "propertyCode": "conductivity",
        "locationCode": "BACAX",
        "deviceCategoryCode": "CTD",
    }
    expected_keys = {
        "cvTerm": dict,
        "description": str,
        "hasDeviceData": bool,
        "hasPropertyData": bool,
        "propertyCode": str,
        "propertyName": str,
        "uom": str,
    }

    expected_keys_cv_term_uom = {
        "uri": str,
        "vocabulary": str,
    }

    data = requester.getProperties(params)

    assert len(data) > 0, "Valid properties test should return at least 1 row."

    util.assert_dict_key_types(data[0], expected_keys)
    util.assert_dict_key_types(data[0]["cvTerm"]["uom"][0], expected_keys_cv_term_uom)
