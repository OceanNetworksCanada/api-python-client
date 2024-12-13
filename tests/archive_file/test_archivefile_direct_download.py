import os


def test_valid_params_one_page(requester, params_location, util):
    data = requester.getArchivefile(params_location)
    result = requester.downloadDirectArchivefile(params_location)

    assert util.get_download_files_num(requester) == len(data["files"])

    assert result["stats"]["fileCount"] == len(data["files"])


def test_valid_params_multiple_pages(requester, params_location_multiple_pages, util):
    result = requester.downloadDirectArchivefile(params_location_multiple_pages)

    assert (
        util.get_download_files_num(requester)
        == params_location_multiple_pages["rowLimit"]
    )

    assert result["stats"]["fileCount"] == params_location_multiple_pages["rowLimit"]


def test_valid_params_overwrite_zero_file_size(
    requester, params_location_single_file, util
):
    filename = "BPR-Folger-59_20191126T000000.000Z.txt"

    file_path = requester.outPath / filename

    # Touch an empty file
    with open(file_path, "w"):
        pass

    # Case when downloading failed, leaving an empty file behind
    assert os.path.getsize(file_path) == 0

    requester.downloadDirectArchivefile(params_location_single_file, overwrite=False)

    assert (
        os.path.getsize(file_path) != 0
    ), "0-size file should be overwritten even if overwrite is False"
