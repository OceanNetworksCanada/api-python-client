import pytest
import requests


def test_wrong_deviceCategoryCode(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getDataProducts(filters={"deviceCategoryCode": "XYZ123"})
