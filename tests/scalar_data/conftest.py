import pytest


@pytest.fixture
def params_device():
    return {
        "deviceCode": "BPR-Folger-59",
        "dateFrom": "2019-11-23T00:00:00.000Z",
        "dateTo": "2019-11-23T00:01:00.000Z",
        "rowLimit": 80000,
    }


@pytest.fixture
def params_location():
    return {
        "locationCode": "NCBC",
        "deviceCategoryCode": "BPR",
        "propertyCode": "seawatertemperature,totalpressure",
        "dateFrom": "2019-11-23T00:00:00.000Z",
        "dateTo": "2019-11-23T00:01:00.000Z",
        "rowLimit": 80000,
    }
