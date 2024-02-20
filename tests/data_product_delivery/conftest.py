import pytest


@pytest.fixture()
def params() -> dict:
    return {
        "dataProductCode": "TSSP",
        "extension": "png",
        "dateFrom": "2019-08-29",
        "dateTo": "2019-08-30",
        "locationCode": "CRIP.C1",
        "deviceCategoryCode": "CTD",
        "dpo_qualityControl": 1,
        "dpo_resample": "none",
    }
