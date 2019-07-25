# delivery services' tests
from robot.libraries.BuiltIn import BuiltIn
import sys
import os
import json
from onc import ONC
from pathlib import Path
sys.path.append(os.path.join(Path(__file__).parents[2], 'onc'))

# get token from Robot variable
token = BuiltIn().get_variable_value("${TOKEN}")
onc = ONC('992deb20-d806-446b-b59e-f73ad8c8d675', True, True, 'output')


def manualRequestProduct(productCode, ext, locationCode, categoryCode, dateFrom, dateTo):
	# Manually requests data product, doesn't execute or download
	filters = {
		"dataProductCode": productCode,
		"extension": ext,
		"dateFrom": dateFrom,
		"dateTo": dateTo,
		"locationCode": locationCode,
		"deviceCategoryCode": categoryCode,
		"dpo_dataGaps": "0",
		"dpo_qualityControl": "1",
		"dpo_resample": "none"
	}
	return onc.requestDataProduct(filters)

def manualRunProduct(dpRequestId):
	# Manually runs request id
	return onc.runDataProduct(dpRequestId)

def manualDownloadProduct(dpRunId, outPath: str='', resultsOnly: bool=False):
	# Manually downloads runId
	onc.outPath = outPath
	return onc.downloadDataProduct(dpRunId, downloadResultsOnly=resultsOnly)


def orderDataProduct(productCode, ext, locationCode, categoryCode, dateFrom, dateTo, retries, linksOnly, metadata, outPath: str=''):
	# run the full orderDataProduct pipeline to request, wait and download a product
	onc.outPath = outPath
	filters = {
		"dataProductCode": productCode,
		"extension": ext,
		"dateFrom": dateFrom,
		"dateTo": dateTo,
		"locationCode": locationCode,
		"deviceCategoryCode": categoryCode,
	}

	if productCode == "TSSD":
		filters["dpo_dataGaps"] = "0"
		filters["dpo_qualityControl"] = "1"
		filters["dpo_resample"] = "none"
		if (ext == "json"):
			filters["dpo_jsonOutputEncoding"] = "OM"

	if productCode == "TSSP":
		filters["dpo_qualityControl"] = "1"
		filters["dpo_resample"] = "none"
		

	return onc.orderDataProduct(filters, retries, linksOnly, metadata)

def test_getDataProductUrls(onc, filters):
	print('\n9. TEST getDataProductUrls()')
	res = onc.getDataProductUrls(filters)

def test_downloadFile(onc, url):
	print('\n9. TEST downloadFile()')
	res = onc.downloadFile(url)
