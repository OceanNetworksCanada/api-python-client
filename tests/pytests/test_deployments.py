import pytest
import requests

def test_wrong_locationCode(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getDataProducts(filters={"locationCode":"XYZ123"})
