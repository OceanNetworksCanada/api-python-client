def test_valid_params_one_page(requester, params_location, util):
    data = requester.getListByLocation(params_location)
    result = requester.getDirectFiles(params_location)

    assert util.get_download_files_num(requester) == len(data["files"])

    assert result["stats"]["fileCount"] == len(data["files"])


def test_valid_params_multiple_pages(requester, params_location_multiple_pages, util):
    result = requester.getDirectFiles(params_location_multiple_pages)

    assert (
        util.get_download_files_num(requester)
        == params_location_multiple_pages["rowLimit"]
    )

    assert result["stats"]["fileCount"] == params_location_multiple_pages["rowLimit"]
