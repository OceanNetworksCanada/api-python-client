import pytest
import requests


def test_wrong_dataProductCode(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getDataProducts(filters={"dataProductCode": "XYZ123"})
