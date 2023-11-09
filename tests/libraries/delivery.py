# delivery services' tests
from env_variable import token

from onc.onc import ONC

# get token from Robot variable
onc = ONC(token, True, True, 'output')


def manualRequestProduct(filters: dict):
	# Manually requests data product, doesn't execute or download
	return onc.requestDataProduct(filters)


def manualRunProduct(dpRequestId: int):
	# Manually runs request id
	return onc.runDataProduct(dpRequestId)


def manualDownloadProduct(dpRunId: int, outPath: str='', resultsOnly: bool=False):
	# Manually downloads runId
	onc.outPath = outPath
	return onc.downloadDataProduct(dpRunId, downloadResultsOnly=resultsOnly)


def test_getDataProductUrls(onc, filters):
	print('\n9. TEST getDataProductUrls()')
	res = onc.getDataProductUrls(filters)


def test_downloadFile(onc, url):
	print('\n9. TEST downloadFile()')
	res = onc.downloadFile(url)
