import pytest
import requests


def test_invalid_param_value(requester):
    with pytest.raises(requests.HTTPError, match=r"API Error 96"):
        requester.getFile("FAKEFILE.XYZ")


def test_invalid_params_missing_required(requester):
    with pytest.raises(requests.HTTPError, match=r"API Error 128"):
        requester.getFile()


def test_valid_params(requester, util):
    filename = "BPR-Folger-59_20191123T000000.000Z.txt"

    requester.getFile(filename)

    assert (requester.outPath / filename).exists()

    with pytest.raises(FileExistsError):
        requester.getFile(filename)

    requester.getFile(filename, overwrite=True)

    assert util.get_download_files_num(requester) == 1
