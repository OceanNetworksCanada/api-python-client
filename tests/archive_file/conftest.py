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


@pytest.fixture
def params_location_single_file(params_location):
    # Returned archivefile name should be BPR-Folger-59_20191126T000000.000Z.txt
    return params_location | {"dateFrom": "2019-11-26", "dateTo": "2019-11-27"}
