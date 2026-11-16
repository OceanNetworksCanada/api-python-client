import pytest
import requests


@pytest.fixture
def params_multiple_pages(params_device):
    # rowLimit should be less than the total number of rows.
    return params_device | {"rowLimit": 25}


def test_invalid_param_value(requester, params_device, err_400):
    params_invalid_param_value = params_device | {"deviceCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=err_400):
        requester.getScalardata(params_invalid_param_value)


def test_invalid_param_name(requester, params_device, err_400):
    params_invalid_param_name = params_device | {"deviceCodes": "BPR-Folger-59"}
    with pytest.raises(requests.HTTPError, match=err_400):
        requester.getScalardata(params_invalid_param_name)


def test_no_data(requester, params_device):
    params_no_data = params_device | {"dateFrom": "2000-01-01", "dateTo": "2000-01-02"}
    data = requester.getScalardata(params_no_data)

    assert data["sensorData"] is None


def test_different_date_format_all_pages(requester, params_multiple_pages):
    params_different_date_format = params_multiple_pages | {
        "dateFrom": "2019-11-23T23:59:00.000Z",
        "dateTo": "2019-11-24",
    }
    requester.getScalardata(params_different_date_format, allPages=True)


def test_valid_params_one_page(requester, params_device, params_multiple_pages):
    data = requester.getScalardata(params_device)
    data_all_pages = requester.getScalardata(params_multiple_pages, allPages=True)

    assert (
        _get_row_num(data) > params_multiple_pages["rowLimit"]
    ), "Test should return at least `rowLimit` rows for each sensor."

    assert data["next"] is None, "Test should return only one page."

    assert (
        data_all_pages["sensorData"][0]["data"] == data["sensorData"][0]["data"]
    ), "Test should concatenate rows for all pages."

    assert data_all_pages["next"] is None, "Test should return only one page."


def test_valid_params_multiple_pages(requester, params_multiple_pages):
    data = requester.getScalardata(params_multiple_pages)

    assert (
        _get_row_num(data) == params_multiple_pages["rowLimit"]
    ), "Test should only return `rowLimit` rows for each sensor."

    assert data["next"] is not None, "Test should return multiple pages."


def test_valid_params_multiple_pages_object_format(
    requester, params_device, params_multiple_pages
):
    object_format = {"outputFormat": "object"}
    data = requester.getScalardata(params_device | object_format)
    data_all_pages = requester.getScalardata(
        params_multiple_pages | object_format, allPages=True
    )

    assert isinstance(data_all_pages["sensorData"][0]["data"], list)
    assert (
        data_all_pages["sensorData"][0]["data"] == data["sensorData"][0]["data"]
    ), "Test should concatenate rows for all pages."
    assert data_all_pages["next"] is None, "Test should return only one page."


def test_production_multiple_pages_with_missing_sensors(requester):
    if not requester.production:
        pytest.skip("This regression dataset is only available in production")

    # It actually only returns 200 rows.
    params = {
        "deviceCode": "NANOMETRICSTITANEA000788",
        "dateFrom": "2026-11-01T07:00:00.000Z",
        "dateTo": "2026-11-01T07:05:00.000Z",
        "rowLimit": 1000,
    }

    # Confirm the two pages reproduce sensors disappearing on the second page.
    first_page = requester.getScalardata(params)
    assert first_page["next"] is not None, "Regression data must span multiple pages"
    second_page = requester.getScalardata(first_page["next"]["parameters"])
    assert second_page["next"] is None, "Regression data should have two pages"

    first_sensors = {s["sensorCode"]: s["data"] for s in first_page["sensorData"]}
    second_sensors = {s["sensorCode"]: s["data"] for s in second_page["sensorData"]}
    missing_sensors = first_sensors.keys() - second_sensors.keys()
    assert {"clock", "period", "amplitude"} <= missing_sensors
    assert second_sensors.keys() <= first_sensors.keys()

    # All sensors and readings from both pages must be present in the merged result.
    result = requester.getScalardata(params, allPages=True)
    assert result["next"] is None
    result_sensors = {s["sensorCode"]: s["data"] for s in result["sensorData"]}
    assert result_sensors.keys() == first_sensors.keys()
    for code, first_data in first_sensors.items():
        for key in first_data:
            expected = first_data[key] + second_sensors.get(code, {}).get(key, [])
            assert result_sensors[code][key] == expected


def test_production_multiple_pages_with_new_sensors(requester):
    if not requester.production:
        pytest.skip("This regression dataset is only available in production")

    params = {
        "deviceCode": "NANOMETRICSTITANEA000788",
        "dateFrom": "2026-11-01T09:00:00.000Z",
        "dateTo": "2026-11-01T09:06:00.000Z",
        "rowLimit": 1000,
    }

    # The sensors begin reporting on the second page.
    first_page = requester.getScalardata(params)
    assert first_page["next"] is not None, "Regression data must span multiple pages"
    second_page = requester.getScalardata(first_page["next"]["parameters"])
    assert second_page["next"] is None, "Regression data should have two pages"

    first_sensors = {s["sensorCode"]: s["data"] for s in first_page["sensorData"]}
    second_sensors = {s["sensorCode"]: s["data"] for s in second_page["sensorData"]}
    new_sensors = second_sensors.keys() - first_sensors.keys()
    assert {"clock", "period", "amplitude"} <= new_sensors

    # The combined response must include each sensor and its readings from both pages.
    result = requester.getScalardata(params, allPages=True)
    assert result["next"] is None
    result_sensors = {s["sensorCode"]: s["data"] for s in result["sensorData"]}
    assert result_sensors.keys() == first_sensors.keys() | second_sensors.keys()
    for code, data in result_sensors.items():
        for key in data:
            expected = first_sensors.get(code, {}).get(key, [])
            expected = expected + second_sensors.get(code, {}).get(key, [])
            assert data[key] == expected


def _get_row_num(data):
    return len(data["sensorData"][0]["data"]["values"])
