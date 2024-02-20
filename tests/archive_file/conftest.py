import pytest


@pytest.fixture
def params_location():
    return {
        "locationCode": "NCBC",
        "deviceCategoryCode": "BPR",
        "dateFrom": "2019-11-23",
        "dateTo": "2019-11-26",
        "fileExtension": "txt",
        "rowLimit": 80000,
        "page": 1,
    }


@pytest.fixture
def params_location_multiple_pages(params_location):
    # rowLimit should be less than the total number of rows.
    return params_location | {"rowLimit": 2}
