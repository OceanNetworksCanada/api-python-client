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
    A wrapper class for Oceans 3.0 API requests.

    All the client library's functionality is provided as methods of this class.

    Parameters
    ----------
    token : str
        The ONC API token, which could be retrieved at https://data.oceannetworks.ca/Profile once logged in.
    production : boolean, default True
        Whether the ONC Production server URL is used for service requests.

        - True: Use the production server.
        - False: Use the internal ONC test server (reserved for ONC staff IP addresses).
    showInfo : boolean, default False
        Whether verbose script messages are displayed, such as request url and processing time information.

        - True: Print all information and debug messages (intended for debugging).
        - False: Only print information messages.
    outPath : str | Path, default "output"
        The directory that files are saved to (relative to the current directory) when downloading files.
        The directory will be created if it does not exist during the download.
    timeout : int, default 60
        Number of seconds before a request to the API is canceled due to a timeout.

    Examples
    --------
    >>> from onc import ONC
    >>> onc = ONC("YOUR_TOKEN_HERE")  # doctest: +SKIP
    >>> onc = ONC("YOUR_TOKEN_HERE", showInfo=True, outPath="onc-files")  # doctest: +SKIP
    """  # noqa: E501

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
        self.production = production
        self.outPath = outPath

        # Create service objects
        self.discovery = _OncDiscovery(self)
        self.delivery = _OncDelivery(self)
        self.realTime = _OncRealTime(self)
        self.archive = _OncArchive(self)

    @property
    def outPath(self) -> Path:
        """
        Return the resolved directory path that files are saved to.

        The setter method can take either `str` or `Path` as the parameter.
        """
        return self._out_path

    @outPath.setter
    def outPath(self, outPath: str | Path) -> None:
        self._out_path = Path(outPath).resolve()

    @property
    def production(self) -> bool:
        """
        Return whether the test is against the Production environment or not.
        """
        return self._production

    @production.setter
    def production(self, is_production: bool) -> None:
        self._production = is_production

        if is_production:
            self.baseUrl = "https://data.oceannetworks.ca/"
        else:
            self.baseUrl = "https://qa.oceannetworks.ca/"

    def print(self, obj, filename: str = "") -> None:
        """
        Pretty print a collection to the console or a file.

        Mainly used to print the results returned by other class methods.

        Parameters
        ----------
        obj: Any
            Any collection, including scalar values, dictionaries and lists (i.e. those returned by other class methods)
        filename : str, default ""
            The filename that is used when saving the json file. It is relative to ``self._out_path``.
            The ``.json`` extension could be omitted.

            - if not empty, save the output to the file.
            - if empty, print the output to the console.
        Examples
        --------
        >>> result = onc.getLocations()  # doctest: +SKIP
        >>> onc.print(result)  # doctest: +SKIP
        """  # noqa: E501
        text = json.dumps(obj, indent=4)
        if filename == "":
            print(text)
        else:
            filePath = self._out_path / filename
            filePath = filePath.with_suffix(".json")

            with open(filePath, "w+") as file:
                file.write(text)

    def formatUtc(self, dateString: str = "now") -> str:
        """
        Format the provided date string as an ISO8601 UTC date string.

        The ISO8601 UTC date format is required by the API.

        Parameters
        ----------
        dateString: str, default "now"
            A string that represents a date & time in any of the formats
            described in http://labix.org/python-dateutil#head-c0e81a473b647dfa787dc11e8c69557ec2c3ecd2.
            Examples are:

            - "2016-12-04"
            - "2016-Dec-04, 12:00:00"
            - "2016 Dec 04 03:00 PM"
            - "now" (returns current UTC date & time)
        Examples
        --------
        >>> onc.formatUtc("2019-Sept-09 03:00 PM")
        '2019-09-09T15:00:00.000Z'
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
        Return locations.

        The API endpoint is ``/locations``.

        Return a list of location names and location codes.

        See https://data.oceannetworks.ca/OpenAPI#get-/locations
        for usage and available query string parameters.

        Parameters
        ----------
        filters : dict, optional
            Query string parameters in the API request. Return all locations available if None.

            Supported parameters are:

            - locationCode
            - deviceCategoryCode
            - propertyCode
            - dataProductCode
            - dateFrom
            - dateTo
            - locationName
            - deviceCode
            - includeChildren

        Returns
        -------
        list of dict
            API response. Each location returned in the list is a dict with the following structure.

            - deployments: int
            - locationName: str
            - depth: float
            - bbox: dict
                - bbox.maxDepth: float
                - bbox.maxLat: float
                - bbox.maxLon: float
                - bbox.minDepth: float
                - bbox.minLat: float
                - bbox.minLon: float
            - description: str
            - hasDeviceData: bool
            - lon: float
            - locationCode: str
            - hasPropertyData: bool
            - lat: float
            - dataSearchURL: str

            Check https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms for more information.

        Examples
        --------
        >>> params = {
        ...     "locationCode": "FGPD",
        ...     "dateFrom": "2005-09-17T00:00:00.000Z",
        ...     "dateTo": "2020-09-17T13:00:00.000Z",
        ... }  # doctest: +SKIP
        >>> onc.getLocations(params)  # doctest: +SKIP
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
        Return a location tree.

        The API endpoint is ``/locations/tree``.

        Return a hierarchical representation of the ONC Search Tree Nodes.
        The Search Tree is used in Oceans 3.0 to organize instruments and variables by location
        so that users can easily drill down by place name or mobile platform name
        to find the instruments or properties they are interested in.

        See https://data.oceannetworks.ca/OpenAPI#get-/locations/tree
        for usage and available query string parameters.

        Parameters
        ----------
        filters : dict, optional
            Query string parameters in the API request. Return a tree of all available locations if None.

            Supported parameters are:

            - locationCode
            - deviceCategoryCode
            - propertyCode
            - dataProductCode
            - dateFrom
            - dateTo
            - locationName
            - deviceCode

        Returns
        ------
        list of dict
            API response. Each location returned in the list is a dict with the following structure.

            - locationName: str
            - children: list of dict | None
            - description: string
            - hasDeviceData: bool
            - locationCode: str
            - hasPropertyData: bool

            Check https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms for more information.

        Examples
        --------
        >>> params = {
        ...     "locationCode": "BACCC",
        ... }  # doctest: +SKIP
        >>> onc.getLocationHierarchy(params)  # doctest: +SKIP
        [
            {
                "locationName": "Coral Cliff",
                "children": [
                    {
                        "locationName": "ADCP 2 MHz East",
                        "children": None,
                        "description": "",
                        "hasDeviceData": True,
                        "locationCode": "BACCC.A1",
                        "hasPropertyData": False,
                    },
                    {
                        "locationName": "ADCP 2 MHz West",
                        "children": None,
                        "description": "",
                        "hasDeviceData": True,
                        "locationCode": "BACCC.A2",
                        "hasPropertyData": False,
                    },
                ],
                "description": " The Coral Cliffs are located within Barkley Canyon. At this location, boundary layer flow near steep bathymetry, interaction of currents, and deep-sea corals are observed.",
                "hasDeviceData": False,
                "locationCode": "BACCC",
                "hasPropertyData": True,
            }
        ]
        """  # noqa: E501
        return self.discovery.getLocationHierarchy(filters)

    def getDeployments(self, filters: dict | None = None):
        """
        Return a list of device deployments.

        The API endpoint is ``/deployments``.

        Return all deployments defined in Oceans 3.0 which meet the filter criteria,
        where a deployment is the installation of a device at a location.
        The deployments service assists in knowing when and where specific types of data are available.

        The primary purpose for the deployments service is to find the dates and locations of deployments
        and use the dateFrom and dateTo datetimes when requesting a data product using the ``dataProductDelivery`` web service.

        See https://data.oceannetworks.ca/OpenAPI#get-/deployments
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Query string parameters in the API request. Return all device deployment if None.

            Supported parameters are:

            - locationCode
            - deviceCategoryCode
            - deviceCode
            - propertyCode
            - dateFrom
            - dateTo

        Returns
        -------
        list of dict
            API response. Each deployment returned in the list is a dict with the following structure.

            - begin: str
            - citation: dict
            - depth: float
            - deviceCategoryCode: str
            - deviceCode: str
            - end: str | None
            - hasDeviceData: bool
            - heading: float | None
            - lat: float
            - locationCode: str
            - lon: float
            - pitch: float | None
            - roll: float | None

            Check https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms for more information.

        Examples
        --------
        >>> params = {
        ...     "locationCode": "BACAX",
        ...     "deviceCategoryCode": "CTD",
        ...     "dateFrom": "2015-09-17",
        ...     "dateTo": "2015-09-17T13:00:00.000Z",
        ... }  # doctest: +SKIP
        >>> onc.getDeployments(params)  # doctest: +SKIP
        [
            {
                "begin": "2014-05-09T15:50:42.000Z",
                "citation": {
                    "citation": "Ocean Networks Canada Society. 2015. Barkley Canyon Axis Conductivity Temperature Depth Deployed 2014-05-09. Ocean Networks Canada Society. https://doi.org/10.80242/14d156f2-0146-40e5-a77e-f3637fb6b517.",
                    "doi": "10.80242/14d156f2-0146-40e5-a77e-f3637fb6b517",
                    "landingPageUrl": "https://doi.org/10.80242/14d156f2-0146-40e5-a77e-f3637fb6b517",
                    "queryPid": None,
                },
                "depth": 982.0,
                "deviceCategoryCode": "CTD",
                "deviceCode": "SBECTD16p6002",
                "end": "2015-09-17T12:59:52.000Z",
                "hasDeviceData": True,
                "heading": None,
                "lat": 48.316583,
                "locationCode": "BACAX",
                "lon": -126.050796,
                "pitch": None,
                "roll": None,
            }
        ]
        """  # noqa: E501
        return self.discovery.getDeployments(filters)

    def getDevices(self, filters: dict | None = None):
        """
        Return a list of devices.

        The API endpoint is ``/devices``.

        Return all the devices defined in Oceans 3.0 that meet a set of filter criteria.
        Devices are instruments that have one or more sensors that observe a property or phenomenon
        with a goal of producing an estimate of the value of a property.
        Devices are uniquely identified by a device code and can be deployed at multiple locations during their lifespan.

        The primary purpose of the devices service is to find devices that have the data you are interested in
        and use the deviceCode when requesting a data product using the ``dataProductDelivery`` web service.

        See https://data.oceannetworks.ca/OpenAPI#get-/devices
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Query string parameters in the API request. Return all devices available if None.

            Supported parameters are:

            - locationCode
            - deviceCategoryCode
            - deviceCode
            - propertyCode
            - dateFrom
            - dateTo

        Returns
        -------
        list of dict
            API response. Each device returned in the list is a dict with the following structure.

            - cvTerm: dict
                - cvTerm.device: list of dict
                    - cvTerm.device[].uri: str
                    - cvTerm.device[].vocabulary: str
            - dataRating: list of dict
                - dataRating[].dateFrom: str
                - dataRating[].dateTo: str | None
                - dataRating[].samplePeriod: float
                - dataRating[].sampleSize: int
            - deviceCategoryCode: str
            - deviceCode: str
            - deviceId: int
            - deviceLink: str
            - deviceName: str
            - hasDeviceData: bool

            Check https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms for more information.

        Examples
        --------
        >>> params = {
        ...     "deviceCode": "BPR-Folger-59",
        ...     "dateFrom": "2005-09-17T00:00:00.000Z",
        ...     "dateTo": "2020-09-17T13:00:00.000Z",
        ... }  # doctest: +SKIP
        >>> onc.getDevices(params)  # doctest: +SKIP
        [
            {
                "cvTerm": {
                    "device": [
                        {
                            "uri": "http://vocab.nerc.ac.uk/collection/L22/current/TOOL1652/",
                            "vocabulary": "SeaVoX Device Catalogue",
                        }
                    ]
                },
                "dataRating": [
                    {
                        "dateFrom": "2007-01-01T00:00:00.000Z",
                        "dateTo": None,
                        "samplePeriod": 1.0,
                        "sampleSize": 1,
                    }
                ],
                "deviceCategoryCode": "BPR",
                "deviceCode": "BPR-Folger-59",
                "deviceId": 21503,
                "deviceLink": "https://data.oceannetworks.ca/DeviceListing?DeviceId=21503",
                "deviceName": "NRCan Bottom Pressure Recorder 59",
                "hasDeviceData": True,
            }
        ]
        """  # noqa: E501
        return self.discovery.getDevices(filters)

    def getDeviceCategories(self, filters: dict | None = None):
        """
        Return a list of device categories

        The API endpoint is ``/deviceCategories``.

        Return all device categories defined in Oceans 3.0 that meet a filter criteria.
        A Device Category represents an instrument type classification such as
        CTD (Conductivity, Temperature & Depth Instrument) or BPR (Bottom Pressure Recorder).
        Devices from a category can record data for one or more properties (variables).

        The primary purpose of this service is to find device categories that have the data you want to access;
        the service provides the deviceCategoryCode you can use
        when requesting a data product via the ``dataProductDelivery`` web service.

        See https://data.oceannetworks.ca/OpenAPI#get-/deviceCategories
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Query string parameters in the API request. Return all device categories available if None.

            Supported parameters are:

            - deviceCategoryCode
            - deviceCategoryName
            - description
            - locationCode
            - propertyCode

        Returns
        -------
        list of dict
            API response. Each device category returned in the list is a dict with the following structure.

            - cvTerm: dict
                - cvTerm.deviceCategory: list of dict
                    - cvTerm.deviceCategory[].uri: str
                    - cvTerm.deviceCategory[].vocabulary: str
            - description: str
            - deviceCategoryCode: str
            - deviceCategoryName: str
            - hasDeviceData: bool
            - longDescription: str

            Check https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms for more information.

        Examples
        --------
        >>> params = {
        ...     "deviceCategoryCode": "CTD",
        ...     "deviceCategoryName": "Conductivity",
        ...     "description": "Temperature",
        ... }  # doctest: +SKIP
        >>> onc.getDeviceCategories(params)  # doctest: +SKIP
        [
            {
                "cvTerm": {
                    "deviceCategory": [
                        {
                            "uri": "http://vocab.nerc.ac.uk/collection/L05/current/130/",
                            "vocabulary": "SeaDataNet device categories",
                        }
                    ]
                },
                "description": "Conductivity Temperature (and Depth Sensor)",
                "deviceCategoryCode": "CTD",
                "deviceCategoryName": "Conductivity Temperature Depth",
                "hasDeviceData": True,
                "longDescription": " Conductivity Temperature Depth (CTD) is an instrument package that contains sensors for measuring the conductivity, temperature, and pressure of seawater. Salinity, sound velocity, depth and density are variables that can be derived from sensor measurements. CTDs can carry additional instruments and sensors such as oxygen sensors, turbidity sensors and fluorometers.",
            }
        ]
        """  # noqa: E501
        return self.discovery.getDeviceCategories(filters)

    def getProperties(self, filters: dict | None = None):
        """
        Return a list of properties.

        The API endpoint is ``/properties``.

        Return all properties defined in Oceans 3.0 that meet a filter criteria.
        Properties are observable phenomena (aka, variables) and are the common names given to sensor types
        (i.e., oxygen, pressure, temperature, etc).

        The primary purpose of this service is to find the available properties of the data you want to access;
        the service provides the propertyCode that you can use to request a data product via the ``dataProductDelivery`` web service.

        See https://data.oceannetworks.ca/OpenAPI#get-/properties
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Query string parameters in the API request. Return all properties available if None.

            Supported parameters are:

            - propertyCode
            - propertyName
            - description
            - locationCode
            - deviceCategoryCode
            - deviceCode

        Returns
        -------
        list of dict
            API response. Each property returned in the list is a dict with the following structure.

            - cvTerm: dict
                - cvTerm.property: list of dict
                    - cvTerm.property[].uri: str
                    - cvTerm.property[].vocabulary: str
                - cvTerm.uom: list of dict
                    - cvTerm.uom[].uri: str
                    - cvTerm.uom[].vocabulary: str
            - description: str
            - hasDeviceData: bool
            - hasPropertyData: bool
            - propertyCode: str
            - propertyName: str
            - uom: str

            Check https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms for more information.

        Examples
        --------
        >>> params = {
        ...     "propertyCode": "conductivity",
        ...     "locationCode": "BACAX",
        ...     "deviceCategoryCode": "CTD",
        ... }  # doctest: +SKIP
        >>> onc.getProperties(params)  # doctest: +SKIP
        [
            {
                "cvTerm": {
                    "property": [],
                    "uom": [
                        {
                            "uri": "http://vocab.nerc.ac.uk/collection/P06/current/UECA/",
                            "vocabulary": "BODC data storage units",
                        }
                    ],
                },
                "description": "Conductivity: siemens per metre",
                "hasDeviceData": True,
                "hasPropertyData": True,
                "propertyCode": "conductivity",
                "propertyName": "Conductivity",
                "uom": "S/m",
            }
        ]
        """  # noqa: E501
        return self.discovery.getProperties(filters)

    def getDataProducts(self, filters: dict | None = None):
        """
        Return a list of data products.

        The API endpoint is ``/dataProducts``.

        Return all data products defined in Oceans 3.0 that meet a filter criteria.
        Data Products are downloadable representations of ONC observational data,
        provided in formats that can be easily ingested by analytical or visualization software.

        The primary purpose of this service is to identify which data products and formats (file extensions)
        are available for the locations, devices, device categories or properties of interest.
        Use the `dataProductCode` and `extension` when requesting a data product via the ``dataProductDelivery`` web service.

        See https://data.oceannetworks.ca/OpenAPI#get-/dataProducts
        for usage and available filters.

        Parameters
        ----------
        filters : dict, optional
            Query string parameters in the API request. Return all data products available if None.

            Supported parameters are:

            - dataProductCode
            - extension
            - dataProductName
            - propertyCode
            - locationCode
            - deviceCategoryCode
            - deviceCode

        Returns
        -------
        list of dict
            API response. Each data product returned in the list is a dict with the following structure.

            - dataProductCode: str
            - dataProductName: str
            - dataProductOptions: list of dict
                - dataProductOptions[].allowableRange: list of dict | None
                    - dataProductOptions[].allowableRange.lowerBound: str
                    - dataProductOptions[].allowableRange.onlyIntegers: bool
                    - dataProductOptions[].allowableRange.unitOfMeasure: str | None
                    - dataProductOptions[].allowableRange.upperBound: str
                - dataProductOptions[].allowableValues: list of str
                - dataProductOptions[].defaultValues: str
                - dataProductOptions[].documentation: list of str
                - dataProductOptions[].option: str
                - dataProductOptions[].suboptions: list of dict | None
            - extension: str
            - hasDeviceData: bool
            - hasPropertyData: bool
            - helpDocument: str

            Check https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms for more information.

        Examples
        --------
        >>> params = {
        ...     "dataProductCode": "SHV",
        ... }  # doctest: +SKIP
        >>> onc.getDataProducts(params)  # doctest: +SKIP
        [
            {
                "dataProductCode": "SHV",
                "dataProductName": "Spectrogram For Hydrophone Viewer",
                "dataProductOptions": [
                    {
                        "allowableRange": {
                            "lowerBound": "-160",
                            "onlyIntegers": False,
                            "unitOfMeasure": None,
                            "upperBound": "140",
                        },
                        "allowableValues": ["-1000"],
                        "defaultValue": "-1000",
                        "documentation": [
                            "https://wiki.oceannetworks.ca/display/DP/Spectrogram+Plot+Options"
                        ],
                        "option": "dpo_lowerColourLimit",
                        "suboptions": None,
                    },
                    {
                        "allowableRange": None,
                        "allowableValues": ["0", "1", "2", "3", "4", "5"],
                        "defaultValue": "0",
                        "documentation": [
                            "https://wiki.oceannetworks.ca/display/DP/Spectrogram+Plot+Options"
                        ],
                        "option": "dpo_spectrogramColourPalette",
                        "suboptions": None,
                    },
                    {
                        "allowableRange": {
                            "lowerBound": "-160",
                            "onlyIntegers": False,
                            "unitOfMeasure": None,
                            "upperBound": "140",
                        },
                        "allowableValues": ["-1000"],
                        "defaultValue": "-1000",
                        "documentation": [
                            "https://wiki.oceannetworks.ca/display/DP/Spectrogram+Plot+Options"
                        ],
                        "option": "dpo_upperColourLimit",
                        "suboptions": None,
                    },
                ],
                "extension": "png",
                "hasDeviceData": True,
                "hasPropertyData": False,
                "helpDocument": "https://wiki.oceannetworks.ca/display/DP/146",
            }
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

    def checkDataProduct(self, dpRequestId: int):
        """
        Check status of a requested data product.

        The API endpoint is ``/dataProductDelivery/status``.

        See https://data.oceannetworks.ca/OpenAPI#get-/dataProductDelivery/status
        for usage.

        Parameters
        ----------
        dpRequestId : int
            A dpRequestId returned from calling ``requestDataProduct``.

        Returns
        -------
        dict
            API response.
        """
        return self.delivery.checkDataProduct(dpRequestId)

    def runDataProduct(self, dpRequestId: int, waitComplete: bool = True):
        return self.delivery.runDataProduct(dpRequestId, waitComplete)

    def cancelDataProduct(self, dpRequestId: int):
        """
        Cancel a running data product.

        The API endpoint is ``/dataProductDelivery/cancel``.

        See https://data.oceannetworks.ca/OpenAPI#get-/dataProductDelivery/cancel
        for usage.

        Parameters
        ----------
        dpRequestId : int
            A dpRequestId returned from calling ``requestDataProduct``.

        Returns
        -------
        list of dict
            API response. Each status returned in the list is a dict with the following structure.

            - dpRunId: int
            - status: str
        """  # noqa: E501
        return self.delivery.cancelDataProduct(dpRequestId)

    def restartDataProduct(self, dpRequestId: int, waitComplete: bool = True):
        """
        Restart a cancelled data product.

        The API endpoint is ``/dataProductDelivery/restart``.

        Restart searches cancelled by calling the ``cancelDataProduct`` method.

        See https://data.oceannetworks.ca/OpenAPI#get-/dataProductDelivery/restart
        for usage.

        Parameters
        ----------
        dpRequestId : int
            A dpRequestId returned from calling ``requestDataProduct``.

        Returns
        -------
        list of dict
            API response. Each status returned in the list is a dict with the following structure.

            - dpRunId: int
            - status: str
        """  # noqa: E501
        return self.delivery.restartDataProduct(dpRequestId, waitComplete)

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

    def getSensorCategoryCodes(self, filters: dict):
        """
        Return a list of sensor category codes.

        A helper method for narrowing down the sensorCategoryCodes that are of interest
        prior to the use of the scalardata service.

        Parameters
        ----------
        filters : dict
            Query string parameters in the API request.
            Use the same filters for calling ``getDirectByLocation`` or ``getDirectByDevice``.

        Returns
        -------
        list of dict
            API response. Each sensor category code returned in the list is a dict with the following structure.

            - outputFormat: str
            - sensorCategoryCode: str
            - sensorCode: str
            - sensorName: str
            - unitOfMeasure: str

        Examples
        --------
        >>> params = {
        ...     "locationCode": "NCBC",
        ...     "deviceCategoryCode": "BPR",
        ...     "propertyCode": "seawatertemperature,totalpressure",
        ... }  # doctest: +SKIP
        >>> onc.getSensorCategoryCodes(params)  # doctest: +SKIP
        [
            {
                "outputFormat": "array",
                "sensorCategoryCode": "pressure",
                "sensorCode": "Pressure",
                "sensorName": "Seafloor Pressure",
                "unitOfMeasure": "decibar",
            },
            {
                "outputFormat": "array",
                "sensorCategoryCode": "temperature",
                "sensorCode": "Temperature",
                "sensorName": "Housing Temperature",
                "unitOfMeasure": "C",
            },
            {
                "outputFormat": "array",
                "sensorCategoryCode": "temperature1",
                "sensorCode": "temperature1",
                "sensorName": "Temperature",
                "unitOfMeasure": "C",
            },
            {
                "outputFormat": "array",
                "sensorCategoryCode": "temperature2",
                "sensorCode": "temperature2",
                "sensorName": "P-Sensor Temperature",
                "unitOfMeasure": "C",
            },
        ]
        """  # noqa: E501
        return self.realTime.getSensorCategoryCodes(filters)

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
