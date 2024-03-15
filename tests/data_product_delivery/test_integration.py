import pytest


def test_valid_manual(requester, params, expected_keys_download_results, util):
    """
    Test request -> status -> run -> download -> status.

    """
    request_id = requester.requestDataProduct(params)["dpRequestId"]
    data_status_before_download = requester.checkDataProduct(request_id)

    assert data_status_before_download["searchHdrStatus"] == "OPEN"

    run_id = requester.runDataProduct(request_id)["runIds"][0]
    data = requester.downloadDataProduct(run_id)

    assert (
        len(data) == 3
    ), "The first two are png files, and the third one is the metadata."

    assert data[0]["status"] == "complete"
    assert data[0]["index"] == "1"
    assert data[0]["downloaded"] is True

    assert data[2]["status"] == "complete"
    assert data[2]["index"] == "meta"
    assert data[2]["downloaded"] is True

    assert util.get_download_files_num(requester) == 3

    util.assert_dict_key_types(data[0], expected_keys_download_results)

    data_status_after_download = requester.checkDataProduct(request_id)

    assert data_status_after_download["searchHdrStatus"] == "COMPLETED"


def test_valid_cancel_restart(requester, params, expected_keys_download_results, util):
    """
    Test request -> run -> cancel -> download (fail) -> restart -> download.

    """
    request_id = requester.requestDataProduct(params)["dpRequestId"]
    run_id = requester.runDataProduct(request_id, waitComplete=False)["runIds"][0]
    data_cancel = requester.cancelDataProduct(request_id)

    assert data_cancel == [{"dpRunId": run_id, "status": "cancelled"}]

    # Uncomment after backend fixes the issue that
    # this 400 error response does not contain "errors" key
    # with pytest.raises(requests.HTTPError, match=r"API Error XXX"):
    with pytest.raises(KeyError):
        requester.downloadDataProduct(run_id)

    run_id_2 = requester.restartDataProduct(request_id)["runIds"][0]
    assert run_id_2 == run_id
    data = requester.downloadDataProduct(run_id)

    assert (
        len(data) == 3
    ), "The first two are png files, and the third one is the metadata."

    assert util.get_download_files_num(requester) == 3

    util.assert_dict_key_types(data[0], expected_keys_download_results)
