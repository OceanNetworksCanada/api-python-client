import pytest
import requests


def test_invalid_param_value(requester):
    params_invalid_param_value = {"dataProductCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDataProducts(params_invalid_param_value)


def test_invalid_param_name(requester):
    params_invalid_param_name = {"dataProductCodes": "HSD"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getDataProducts(params_invalid_param_name)


def test_no_data(requester):
    params_no_data = {
        "dataProductCode": "HSD",
        "extension": "txt",
    }

    with pytest.raises(requests.HTTPError, match=r"404 Client Error"):
        requester.getDataProducts(params_no_data)


def test_valid_params(requester, util):
    params = {
        "dataProductCode": "HSD",
        "extension": "png",
    }
    expected_keys = {
        "dataProductCode": str,
        "dataProductName": str,
        "dataProductOptions": list,
        "extension": str,
        "hasDeviceData": bool,
        "hasPropertyData": bool,
        "helpDocument": str,
    }

    expected_keys_data_product_options = {
        "allowableRange": dict,
        "allowableValues": list,
        "defaultValue": str,
        "documentation": list,
        "option": str,
        "suboptions": None,
    }
    expected_keys_data_product_options_allowable_range = {
        "lowerBound": str,
        "onlyIntegers": bool,
        "unitOfMeasure": str,
        "upperBound": str,
    }

    data = requester.getDataProducts(params)

    assert len(data) > 0, "Valid properties test should return at least 1 row."

    util.assert_dict_key_types(data[0], expected_keys)
    util.assert_dict_key_types(
        data[0]["dataProductOptions"][6], expected_keys_data_product_options
    )
    util.assert_dict_key_types(
        data[0]["dataProductOptions"][6]["allowableRange"],
        expected_keys_data_product_options_allowable_range,
    )
