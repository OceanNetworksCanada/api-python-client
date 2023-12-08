import pytest
import requests


def test_wrong_deviceCode(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getDataProducts(filters={"deviceCode": "XYZ123"})
