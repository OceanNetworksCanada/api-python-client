import pytest
import requests


def test_download_wrong_runID(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.downloadDataProduct(1234567890)


def test_run_wrong_runID(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.runDataProduct(1234567890)
