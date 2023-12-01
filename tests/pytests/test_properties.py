import pytest
import requests

def test_wrong_propertyCode(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 127"):
        requester.getLocations(filters={"propertyCode":"XYZ123"})
