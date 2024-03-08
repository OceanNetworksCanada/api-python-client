import pytest


@pytest.fixture
def expected_keys():
    return {
        "outputFormat": str,
        "sensorCategoryCode": str,
        "sensorCode": str,
        "sensorName": str,
        "unitOfMeasure": str,
    }


def test_valid_params_by_location(requester, params_location, expected_keys, util):
    data = requester.getSensorCategoryCodes(params_location)
    util.assert_dict_key_types(data[0], expected_keys)


def test_valid_params_by_device(requester, params_device, expected_keys, util):
    data = requester.getSensorCategoryCodes(params_device)
    util.assert_dict_key_types(data[0], expected_keys)
