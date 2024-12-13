import os

import pytest
import requests


def test_invalid_param_value(requester):
    with pytest.raises(requests.HTTPError, match=r"API Error 96"):
        requester.downloadArchivefile("FAKEFILE.XYZ")


def test_invalid_params_missing_required(requester):
    with pytest.raises(requests.HTTPError, match=r"API Error 128"):
        requester.downloadArchivefile()


def test_valid_params(requester, util):
    filename = "BPR-Folger-59_20191123T000000.000Z.txt"

    requester.downloadArchivefile(filename)

    assert (requester.outPath / filename).exists()

    with pytest.raises(FileExistsError):
        requester.downloadArchivefile(filename)

    requester.downloadArchivefile(filename, overwrite=True)

    assert util.get_download_files_num(requester) == 1


def test_valid_params_overwrite_zero_file_size(requester):
    filename = "BPR-Folger-59_20191123T000000.000Z.txt"

    file_path = requester.outPath / filename

    # Touch an empty file
    with open(file_path, "w"):
        pass

    # Case when downloading failed, leaving an empty file behind
    assert os.path.getsize(file_path) == 0

    requester.downloadArchivefile(filename, overwrite=False)

    assert (
        os.path.getsize(file_path) != 0
    ), "0-size file should be overwritten even if overwrite is False"
