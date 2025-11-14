import pytest
import requests


@pytest.fixture
def params():
    return {
        "locationCode": "NCBC",
        "deviceCategoryCode": "BPR",
        "dateFrom": "2019-11-23",
        "dateTo": "2019-11-30",
    }


def test_invalid_param_value(requester, params):
    params_invalid_param_value = params | {"locationCode": "INVALID"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getDataAvailability(params_invalid_param_value)


def test_valid_params(requester, params, util):
    data = requester.getDataAvailability(params)

    expected_keys = {
        "availableDataProducts": list,
        "messages": list,
        "next": None,
        "queryUrl": str,
    }

    expected_keys_available_data_products = {
        "averageFileCoverage": float,
        "dataProductCode": str,
        "dateFrom": str,
        "dateTo": str,
        "deviceCode": str,
        "extension": str,
        "fileCount": int,
        "maxFileCoverage": float,
        "maxFileCoverageDate": str,
        "minFileCoverage": float,
        "minFileCoverageDate": str,
        "totalFileSize": int,
        "totalUncompressedFileSize": int,
    }

    util.assert_dict_key_types(data, expected_keys)
    util.assert_dict_key_types(
        data["availableDataProducts"][0], expected_keys_available_data_products
    )
