import pytest
import requests


def test_invalid_param_value(requester, params):
    params_invalid_param_value = params | {"dataProductCode": "XYZ123"}
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.orderDataProduct(params_invalid_param_value)


def test_valid_default(requester, params, expected_keys_download_results, util):
    data = requester.orderDataProduct(params)

    assert (
        len(data["downloadResults"]) == 3
    ), "The first two are png files, and the third one is the metadata."

    assert data["downloadResults"][0]["status"] == "complete"
    assert data["downloadResults"][0]["index"] == "1"
    assert data["downloadResults"][0]["downloaded"] is True

    assert data["downloadResults"][2]["status"] == "complete"
    assert data["downloadResults"][2]["index"] == "meta"
    assert data["downloadResults"][2]["downloaded"] is True

    assert util.get_download_files_num(requester) == 3

    util.assert_dict_key_types(
        data["downloadResults"][0], expected_keys_download_results
    )


def test_valid_no_metadata(requester, params, expected_keys_download_results, util):
    data = requester.orderDataProduct(params, includeMetadataFile=False)

    # The first two are png files
    assert len(data["downloadResults"]) == 2

    assert data["downloadResults"][0]["status"] == "complete"
    assert data["downloadResults"][0]["index"] == "1"
    assert data["downloadResults"][0]["downloaded"] is True

    assert data["stats"]["totalSize"] != 0

    assert util.get_download_files_num(requester) == 2, "The first two are png files."

    util.assert_dict_key_types(
        data["downloadResults"][0], expected_keys_download_results
    )


def test_valid_results_only(requester, params, expected_keys_download_results, util):
    data = requester.orderDataProduct(params, downloadResultsOnly=True)

    assert (
        len(data["downloadResults"]) == 3
    ), "The first two are png files, and the third one is the metadata."

    assert data["downloadResults"][0]["status"] == "complete"
    assert data["downloadResults"][0]["index"] == "1"
    assert data["downloadResults"][0]["downloaded"] is False

    assert data["downloadResults"][2]["status"] == "complete"
    assert data["downloadResults"][2]["index"] == "meta"
    assert data["downloadResults"][2]["downloaded"] is False

    assert (
        util.get_download_files_num(requester) == 0
    ), "No files should be downloaded when download_results_only is True."

    util.assert_dict_key_types(
        data["downloadResults"][0], expected_keys_download_results
    )
