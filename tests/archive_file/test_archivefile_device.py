import pytest
import requests


@pytest.fixture
def params():
    return {
        "deviceCode": "BPR-Folger-59",
        "dateFrom": "2019-11-23",
        "dateTo": "2019-11-26",
        "fileExtension": "txt",
        "rowLimit": 80000,
        "page": 1,
    }


@pytest.fixture
def params_multiple_pages(params):
    # rowLimit should be less than the total number of rows.
    return params | {"rowLimit": 2}


def test_invalid_param_value(requester, params):
    params_invalid_param_value = params | {"deviceCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.getArchivefile(params_invalid_param_value)


def test_invalid_params_missing_required(requester, params):
    del params["deviceCode"]
    with pytest.raises(ValueError):
        requester.getArchivefile(params)


def test_invalid_param_name(requester, params):
    params_invalid_param_name = params | {"deviceCodes": "BPR-Folger-59"}
    with pytest.raises(requests.HTTPError, match=r"API Error 129"):
        requester.getArchivefile(params_invalid_param_name)


def test_no_data(requester, params):
    params_no_data = params | {"dateFrom": "2000-01-01", "dateTo": "2000-01-02"}
    data = requester.getArchivefile(params_no_data)

    assert len(data["files"]) == 0


def test_valid_params_one_page(requester, params, params_multiple_pages):
    data = requester.getArchivefile(params)
    data_all_pages = requester.getArchivefile(params_multiple_pages, allPages=True)

    assert (
        len(data["files"]) > params_multiple_pages["rowLimit"]
    ), "Test should return at least `rowLimit` rows."

    assert data["next"] is None, "Test should return only one page."

    assert (
        data_all_pages["files"] == data["files"]
    ), "Test should concatenate rows for all pages."

    assert data_all_pages["next"] is None, "Test should return only one page."


def test_valid_params_multiple_pages(requester, params_multiple_pages):
    data = requester.getArchivefile(params_multiple_pages)

    assert (
        len(data["files"]) == params_multiple_pages["rowLimit"]
    ), "Test should only return `rowLimit` rows."

    assert data["next"] is not None, "Test should return multiple pages."
