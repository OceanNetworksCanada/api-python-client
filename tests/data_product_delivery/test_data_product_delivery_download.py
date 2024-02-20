import pytest
import requests


def test_invalid_run_id(requester):
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.downloadDataProduct(1234567890)
