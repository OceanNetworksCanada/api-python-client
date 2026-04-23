import pytest
import requests


def test_invalid_request_id(requester, err_400):
    with pytest.raises(requests.HTTPError, match=err_400):
        requester.restartDataProduct(1234567890)
