import pytest
import requests


def test_invalid_run_id(requester, err_400):
    with pytest.raises(requests.HTTPError, match=err_400):
        requester.downloadDataProduct(1234567890)
