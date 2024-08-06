<h1 align="center">
<img src="https://www.oceannetworks.ca/svg/logo.svg" width="300">
</h1><br>

# onc: client library for accessing Oceans 3.0 API

[![PyPI Latest Release](https://img.shields.io/pypi/v/onc.svg)](https://pypi.org/project/onc/)
[![PyPI Supported Versions](https://img.shields.io/pypi/pyversions/onc.svg)](https://pypi.org/project/onc/)
[![License - Apache 2.0](https://img.shields.io/pypi/l/onc.svg)](https://github.com/OceanNetworksCanada/api-python-client/blob/main/LICENSE.txt)
[![Frontiers in Marine Science Paper](https://img.shields.io/badge/DOI-10.3389%2Ffmars.2022.806452-blue)](https://doi.org/10.3389/fmars.2022.806452)

onc is a Python client library that facilitates access to scientific data hosted by [Ocean Networks Canada](https://oceannetworks.ca)
through the [Oceans 3.0 API](https://data.oceannetworks.ca/OpenAPI) public web services.
It can help you explore and download our data, by consuming our
_[discovery](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#discovery-methods)_,
_[data product download](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#data-product-download-methods)_,
_[archive file download](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#archive-file-download-methods)_, and
_[near real-time data access](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#near-real-time-data-access-methods)_ services.

# Getting Started

## Installation

onc can be installed from PyPI:

```shell
pip install onc
```

## Obtaining a token

A unique Oceans 3.0 API token is required to access our data.
To obtain a token, follow the steps below:

1. Register for an Oceans 3.0 account at <https://data.oceannetworks.ca/Registration>.

2. Log into your account at <https://data.oceannetworks.ca> by clicking the Log In link.

3. Click the _Profile_ link (top right corner) to access your account profile.

4. Access the _Web Services API_ tab and click _Copy Token_.

5. If you forget your token, you can always find it again in your Oceans 3.0 account profile.

## Searching with discovery methods

To download ONC data, you need to specify the type of data you require
and where in particular (i.e. location, device) it originates from.

In the Oceans 3.0 API, there's a unique code that identifies every location, device, property, data product type, etc.
Include these codes in a group of filters (these will be used as URL parameters when making HTTP requests)
that determine the data you're interested in.

Discovery methods allow you to explore the hierarchy of the ONC database to obtain the codes for your filters
(they work like a "search" function).

The example below uses the `getLocations` method to search for locations that include "Burrard" in their name (i.e. "Burrard Inlet"):

```python
from onc import ONC

onc = ONC("YOUR_TOKEN_HERE")

onc.getLocations({"locationName": "Burrard"})
```

The previous code prints a list with locations that match the search filters provided.
Each location in the list includes a _dataSearchURL_ that points to the Data Search Tool,
and a _locationCode_ ("BIPP" and "BISS" in this example) that can be used to continue searching "inside" it,
as in the following example:

```python
onc.getDeviceCategories({"locationCode": "BIIP"})
onc.getDataProducts({"locationCode": "BIIP", "deviceCategoryCode": "CTD"})
```

Check more on the _[discovery methods guide](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#discovery-methods)_
and _[code examples](https://oceannetworkscanada.github.io/api-python-client/Code_Examples/index.html)_.

## Downloading data products

Once you determine the exact dictionary of filters that identifies the data you are interested in,
there are multiple methods to download it.

One method is to request the ONC servers to generate a custom data product with the data.
This is done through the data product download methods.

The following example downloads two PNG files with plots for 30 seconds of data from a CTD in Campbell River:

```python
params = {
    "locationCode": "BIIP",
    "deviceCategoryCode": "CTD",
    "dataProductCode": "TSSP",
    "extension": "png",
    "dateFrom": "2019-06-20T00:00:00.000Z",
    "dateTo": "2019-06-20T00:30:00.000Z",
    "dpo_qualityControl": "1",
    "dpo_resample": "none",
}
onc.orderDataProduct(params, includeMetadataFile=False)
```

The filters above include codes for location, deviceCategory, and dataProduct,
as well as the file extension and a time interval (in UTC).
They also include a couple of filters to configure this specific data product type (starting with the "dpo\_" prefix),
which can be obtained from the [Data Product Options](https://wiki.oceannetworks.ca/display/DP/Data+Product+Options) documentation.
You can download more than 120 different [types of data products](https://wiki.oceannetworks.ca/display/O2A/Available+Data+Products) including audio & video.

Check more on the _[data product download methods guide](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#data-product-download-methods)_
and _[code examples](https://oceannetworkscanada.github.io/api-python-client/Code_Examples/Download_Data_Products.html)_.

## Obtaining sensor readings in (near) real-time

Another method to obtain ONC data is by directly obtaining a time series of sensor readings
(available as soon as they reach our database).

In the following example, we obtain 5 seconds of conductivity readings from the CTD at Burrard Inlet:

```python
params = {
    "locationCode": "BIIP",
    "deviceCategoryCode": "CTD",
    "propertyCode": "conductivity",
    "dateFrom": "2019-06-20T00:00:00.000Z",
    "dateTo": "2019-06-20T00:00:05.000Z",
}
onc.getDirectByLocation(params)
```

The result includes matching lists of "values" and "sampleTimes" (increases performance for long time ranges).
We also use the property code "conductivity" to limit results to a specific property available in this CTD.

Check more on the _[near real-time data access methods guide](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#near-real-time-data-access-methods)_
and _[code examples](https://oceannetworkscanada.github.io/api-python-client/Code_Examples/Request_Real_Time_Data.html)_.

## Downloading archived files

ONC scripts auto-generate and archive data products of different types at set time intervals.
You can directly download these data product files from our files archive, as long as you know their unique filename.

In the following example, we get a list of archived files available for a camera at Ridley Island (in a certain time span),
and download one of the files:

```python
params = {
    "locationCode": "RISS",
    "deviceCategoryCode": "VIDEOCAM",
    "dateFrom": "2016-12-01T00:00:00.000Z",
    "dateTo": "2016-12-01T00:05:00.000Z",
}
result = onc.getListByLocation(params, allPages=True)

# download one of the files from result["files"]
onc.getFile("AXISQ6044PTZACCC8E334C53_20161201T000001.000Z.jpg")
```

You can use the method `getFile()` as above to download individual files or the method `getDirectFiles()`
to download all the files that match your filters.

Check more on the _[archive file download methods guide](https://oceannetworkscanada.github.io/api-python-client/API_Guide.html#archive-file-download-methods)_
and _[code examples](https://oceannetworkscanada.github.io/api-python-client/Code_Examples/Download_Archived_Files.html)_.

# Documentation

The client library documentation is hosted on [GitHub Pages](https://oceannetworkscanada.github.io/api-python-client).
For documentation and examples about Oceans 3.0 API, visit the [wiki](https://wiki.oceannetworks.ca/display/O2A/Oceans+3.0+API+Home)
and [OpenAPI](https://data.oceannetworks.ca/OpenAPI) page on the Oceans 3.0 Data Portal website.

# Multithreading issue

We kindly ask users to **not** use too many threads when using threading/multiprocessing libraries on download tasks.
It can cause issues for both server and client and may not appreciably increase download speeds.

# Contributing

All contributions are welcome and appreciated!
Please refer to the [Contributing guide](https://oceannetworkscanada.github.io/api-python-client/contributing.html) before submitting any issues or pull requests.
