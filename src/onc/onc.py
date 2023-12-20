from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

from dateutil import parser
from onc.modules._OncArchive import _OncArchive
from onc.modules._OncDelivery import _OncDelivery
from onc.modules._OncDiscovery import _OncDiscovery
from onc.modules._OncRealTime import _OncRealTime


class ONC:
    """
    Python ONC Api Client Library
    Common library wrapper
    """

    def __init__(
        self,
        token,
        production: bool = True,
        showInfo: bool = False,
        outPath: str | Path = "output",
        timeout: int = 60,
    ):
        self.token = re.sub(r"[^a-zA-Z0-9\-]+", "", token)
        self.showInfo = showInfo
        self.timeout = timeout
        self.baseUrl = "https://data.oceannetworks.ca/"
        self.outPath = ""

        outPath = str(outPath)
        # sanitize outPath
        if len(outPath) > 0:
            outPath = outPath.replace("\\", "/")
            if outPath[-1] == "/":
                outPath = outPath[:-1]
            self.outPath = outPath

        # switch to qa if needed
        if not production:
            self.baseUrl = "https://qa.oceannetworks.ca/"

        # Create service objects
        self.discovery = _OncDiscovery(self)
        self.delivery = _OncDelivery(self)
        self.realTime = _OncRealTime(self)
        self.archive = _OncArchive(self)

    def print(self, obj, filename: str = ""):
        """
        Helper for printing a JSON dictionary to the console or to a file
        @filename: if present, creates the file and writes the output in it
        """
        text = json.dumps(obj, indent=4)
        if filename == "":
            print(text)
        else:
            with open(filename, "w+") as file:
                file.write(text)

    def formatUtc(self, dateString: str = "now"):
        """
        Helper that returns an ISO8601 string for the provided date string
        Most date formats are supported, as explained in: http://labix.org/python-dateutil#head-c0e81a473b647dfa787dc11e8c69557ec2c3ecd2
        A value of "now" returns the current UTC date & time
        Depends on the local system clock
        """
        if dateString == "now":
            return (
                datetime.datetime.utcnow().replace(microsecond=0).isoformat() + ".000Z"
            )
        else:
            objDate = parser.parse(dateString)
            return objDate.replace(microsecond=0).isoformat() + ".000Z"

    # PUBLIC METHOD WRAPPERS

    # Discovery methods

    def getLocations(self, filters: dict | None = None):
        """
        Returns a filtered list of locations.

        The API endpoint is api/locations.

        See https://wiki.oceannetworks.ca/display/O2A/Discovery+methods#Discoverymethods-getLocationsgetLocations
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Filters in the API request. Return all locations available if None.

        Returns
        -------
        list of dict
            API response.

        Examples
        --------
        >>> filters = {
        ...     'locationCode': 'FGPD',
        ...     "dateFrom": "2005-09-17T00:00:00.000Z",
        ...     "dateTo": "2020-09-17T13:00:00.000Z",
        ... }
        >>> onc.getLocations(filters) # doctest: +SKIP
        [
            {
                "deployments": 46,
                "locationName": "Folger Deep",
                "depth": 96.569761,
                "bbox": {
                    "maxDepth": 105.0,
                    "maxLat": 48.814029,
                    "maxLon": -125.274604,
                    "minDepth": 94.0,
                    "minLat": 48.813667,
                    "minLon": -125.28195,
                },
                "description": " Folger Deep is a deep location in Folger Passage near a pillar-like seamount, where productivity and marine mammals are observed.",
                "hasDeviceData": True,
                "lon": -125.280572,
                "locationCode": "FGPD",
                "hasPropertyData": False,
                "lat": 48.813795,
                "dataSearchURL": "https://data.oceannetworks.ca/DataSearch?location=FGPD",
            }
        ]
        """  # noqa: E501
        return self.discovery.getLocations(filters)

    def getLocationHierarchy(self, filters: dict | None = None):
        """
        Returns a filtered tree of locations with their children.

        The API endpoint is api/locations/tree.

        See https://wiki.oceannetworks.ca/pages/viewpage.action?pageId=75170317#Discoverymethods-getLocationHierarchy
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Filters in the API request. Return a tree of all available locations if None.

        Returns
        ------
        list of dict
            API response.

        Examples
        --------
        >>> filters = { 'locationCode': 'STR01' }
        >>> onc.getLocationHierarchy(filters) # doctest: +SKIP
        [
            {
                "locationName": "Neutrino Project Mooring 01 (Yellow)",
                "description": "TBD",
                "hasDeviceData": true,
                "locationCode": "STR01",
                "hasPropertyData": false,
                "children": [
                    {
                        "locationName": "POCAM 110 mab",
                        "children": null,
                        "description": "",
                        "hasDeviceData": true,
                        "locationCode": "STR01.PO1",
                        "hasPropertyData": false
                    },
                    {
                        "locationName": "POCAM 50 mab",
                        "children": null,
                        "description": "",
                        "hasDeviceData": true,
                        "locationCode": "STR01.PO2",
                        "hasPropertyData": false
                    }
                ]
            }
        ]
        """  # noqa: E501
        return self.discovery.getLocationHierarchy(filters)

    def getDeployments(self, filters: dict | None = None):
        """
        Returns a filtered list of deployments.

        The API endpoint is api/deployments.

        See https://wiki.oceannetworks.ca/pages/viewpage.action?pageId=75170317#Discoverymethods-getDeployments
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Filters in the API request. Return all device deployment if None.

        Returns
        -------
        list of dict
            API response.

        Examples
        --------
        >>> filters = { 'deviceCode': 'NORTEKADCP9917' }
        >>> onc.getDeployments(filters) # doctest: +SKIP
        [
            {
                "deviceCode": "NORTEKADCP9917",
                "locationCode": "BACWL",
                "begin": "2012-05-31T20:46:05.000Z",
                "end": "2014-05-10T01:40:00.000Z",
                "hasDeviceData": true,
                "lat": 48.311743,
                "lon": -126.065378,
                "depth": 860.0,
                "heading": null,
                "pitch": null,
                "roll": null
            }
        ]
        """  # noqa: E501
        return self.discovery.getDeployments(filters)

    def getDevices(self, filters: dict | None = None):
        """
        Returns a filtered list of devices.

        The API endpoint is api/devices.

        See https://wiki.oceannetworks.ca/pages/viewpage.action?pageId=75170317#Discoverymethods-getDevices
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Filters in the API request. Return all devices available if None.

        Returns
        -------
        list of dict
            API response.

        Examples
        --------
        >>> filters = {
                'deviceCode': 'BPR-Folger-59',
                'dateFrom': '2005-09-17T00:00:00.000Z',
                'dateTo': '2020-09-17T13:00:00.000Z'
            }
        >>> onc.getDevices(filters) # doctest: +SKIP
        [
            {
                "deviceCode": "BPR-Folger-59",
                "deviceId": 21503,
                "deviceCategoryCode": "BPR",
                "deviceName": "NRCan Bottom Pressure Recorder 59",
                "deviceLink": "https://data.oceannetworks.ca/DeviceListing?DeviceId=21503",
                "hasDeviceData": true,
                "dataRating": [
                    {
                    "dateFrom": "2007-01-01T00:00:00.000Z",
                    "dateTo": null,
                    "samplePeriod": 1,
                    "sampleSize": 1
                    }
                ],
                "cvTerm": {
                    "device": [
                        {
                            "vocabulary": "SeaVoX Device Catalogue",
                            "uri": "http://vocab.nerc.ac.uk/collection/L22/current/TOOL1652/"
                        }
                    ]
                }
            }
        ]
        """  # noqa: E501
        return self.discovery.getDevices(filters)

    def getDeviceCategories(self, filters: dict | None = None):
        """
        Returns a filtered list of device categories.

        The API endpoint is api/deviceCategories.

        See https://wiki.oceannetworks.ca/pages/viewpage.action?pageId=75170317#Discoverymethods-getDeviceCategories
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Filters in the API request. Return all device categories available if None.

        Returns
        -------
        list of dict
            API response.

        Examples
        --------
        >>> filters = { 'locationCode': 'NCBC' }
        >>> onc.getDeviceCategories(filters) # doctest: +SKIP
        [
            {
                "deviceCategoryCode": "CTD",
                "deviceCategoryName": "CTD",
                "description": "Conductivity Temperature (and Depth Sensor)",
                "longDescription": " Conductivity Temperature Depth (CTD) is (...)",
                "hasDeviceData": "true",
                "cvTerm": {
                    "deviceCategory": [
                        {
                           "uri": "http://vocab.nerc.ac.uk/collection/L05/current/130/",
                           "vocabulary": "SeaDataNet device categories"
                        }
                    ]
                }
            }
        ]
        """  # noqa: E501
        return self.discovery.getDeviceCategories(filters)

    def getProperties(self, filters: dict | None = None):
        """
        Returns a filtered list of properties.

        The API endpoint is api/properties.

        See https://wiki.oceannetworks.ca/pages/viewpage.action?pageId=75170317#Discoverymethods-getProperties
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Filters in the API request. Return all properties available if None.

        Returns
        -------
        list of dict
            API response.

        Examples
        --------
        >>> filters = { 'deviceCode': 'BC_POD1_AD2M' }
        >>> onc.getProperties(filters) # doctest: +SKIP
        [
            {
                "propertyCode": "soundspeed",
                "propertyName": "Sound Speed",
                "description": "Sound Speed: sound velocity sensor",
                "uom": "m/s",
                "hasDeviceData": true,
                "hasPropertyData": false,
                "cvTerm": {
                    "property": [],
                    "uom": [
                        {
                            "uri": "http://vocab.nerc.ac.uk/collection/P06/current/UVAA/",
                            "vocabulary": "BODC data storage units"
                        }
                    ]
                }
            },
            (...)
        ]
        """  # noqa: E501
        return self.discovery.getProperties(filters)

    def getDataProducts(self, filters: dict | None = None):
        """
        Returns a filtered list of data products.

        The API endpoint is api/dataProducts.

        See https://wiki.oceannetworks.ca/pages/viewpage.action?pageId=75170317#Discoverymethods-getDataProducts
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Filters in the API request. Return all data products available if None.

        Returns
        -------
        list of dict
            API response.

        Examples
        --------
        >>> filters = {
        ...     'locationCode': 'PHYD',
        ...     'extension': 'mat'
        ... }
        >>> onc.getDataProducts(filters) # doctest: +SKIP
        [
            {
                "dataProductCode": "TSSD",
                "dataProductName": "Time Series Scalar Data",
                "extension": "json",
                "hasDeviceData": true,
                "hasPropertyData": true,
                "helpDocument": "https://wiki.oceannetworks.ca/display/DP/1"
            },
            (...)
        ]
        """  # noqa: E501
        return self.discovery.getDataProducts(filters)

    # Delivery methods

    def orderDataProduct(
        self,
        filters: dict,
        maxRetries: int = 0,
        downloadResultsOnly: bool = False,
        includeMetadataFile: bool = True,
        overwrite: bool = False,
    ):
        return self.delivery.orderDataProduct(
            filters, maxRetries, downloadResultsOnly, includeMetadataFile, overwrite
        )

    def requestDataProduct(self, filters: dict):
        return self.delivery.requestDataProduct(filters)

    def runDataProduct(self, dpRequestId: int, waitComplete: bool = True):
        return self.delivery.runDataProduct(dpRequestId, waitComplete)

    def downloadDataProduct(
        self,
        runId: int,
        maxRetries: int = 0,
        downloadResultsOnly: bool = False,
        includeMetadataFile: bool = True,
        overwrite: bool = False,
    ):
        return self.delivery.downloadDataProduct(
            runId, maxRetries, downloadResultsOnly, includeMetadataFile, overwrite
        )

    # Real-time methods

    def getDirectScalar(self, filters: dict = None, allPages: bool = False):
        # Alias for getDirectByLocation (to be eventually discontinued)
        return self.getDirectByLocation(filters, allPages)

    def getDirectByLocation(self, filters: dict = None, allPages: bool = False):
        return self.realTime.getDirectByLocation(filters, allPages)

    def getDirectByDevice(self, filters: dict = None, allPages: bool = False):
        return self.realTime.getDirectByDevice(filters, allPages)

    def getDirectRawByLocation(self, filters: dict = None, allPages: bool = False):
        return self.realTime.getDirectRawByLocation(filters, allPages)

    def getDirectRawByDevice(self, filters: dict = None, allPages: bool = False):
        return self.realTime.getDirectRawByDevice(filters, allPages)

    # Archive file methods

    def getListByLocation(self, filters: dict = None, allPages: bool = False):
        return self.archive.getListByLocation(filters, allPages)

    def getListByDevice(self, filters: dict = None, allPages: bool = False):
        return self.archive.getListByDevice(filters, allPages)

    def getFile(self, filename: str = "", overwrite: bool = False):
        return self.archive.getFile(filename, overwrite)

    def getDirectFiles(
        self, filters: dict = None, overwrite: bool = False, allPages: bool = False
    ):
        return self.archive.getDirectFiles(filters, overwrite, allPages)
