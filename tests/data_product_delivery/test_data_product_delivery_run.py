import pytest
import requests


def test_invalid_request_id(requester):
    with pytest.raises(requests.HTTPError, match=r"API Error 127"):
        requester.runDataProduct(1234567890)
