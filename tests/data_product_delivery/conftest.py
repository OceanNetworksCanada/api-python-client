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


@pytest.fixture()
def expected_keys_download_results() -> dict:
    return {
        "url": str,
        "status": str,
        "size": int,
        "file": str,
        "index": str,
        "downloaded": bool,
        "requestCount": int,
        "fileDownloadTime": float,
    }
