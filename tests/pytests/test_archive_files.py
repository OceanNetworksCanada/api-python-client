import pytest
import requests


@pytest.fixture
def f_location1():
    return {
        "locationCode": "RISS",
        "deviceCategoryCode": "VIDEOCAM",
        "dateFrom": "2016-12-01T00:00:00.000Z",
        "dateTo": "2016-12-01T01:00:00.000Z"
    }


def test_missing_deviceCategoryCode(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 128"):
        loc_wrong = {
            "dateFrom": "2010-01-01T00:00:00.000Z",
            "dateTo": "2010-01-01T00:02:00.000Z"
        }
        requester.getListByLocation(filters=loc_wrong)

def test_wrong_getFile_filename(requester):
    with pytest.raises(requests.HTTPError, match=r"Error 96"):
        requester.getFile(filename="FAKEFILE.XYZ")

def test_wrong_getList_invalid_filters(requester, f_location1):
    with pytest.raises(requests.HTTPError, match=r"Error 129"):
        requester.getListByDevice(filters=f_location1)
