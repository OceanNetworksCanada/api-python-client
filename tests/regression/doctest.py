"""
Doctest for all the public methods in the onc client library (ONC class).

This file is used for internal regression test every month.
It should be run against QA environment.
If any test failed, update both this file and the corresponding docstring for the tested method.
"""

# ruff: noqa: E501


def test_get_locations(requester):
    params = {
        "locationCode": "FGPD",
        "dateFrom": "2005-09-17T00:00:00.000Z",
        "dateTo": "2020-09-17T13:00:00.000Z",
    }
    result = [
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

    result[0]["dataSearchURL"] = result[0]["dataSearchURL"].replace("data", "qa", 1)

    assert requester.getLocations(params) == result


def test_get_locations_tree(requester):
    params = {
        "locationCode": "BACCC",
    }
    result = [
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

    assert requester.getLocationHierarchy(params) == result


def test_get_deployments(requester):
    params = {
        "locationCode": "BACAX",
        "deviceCategoryCode": "CTD",
        "dateFrom": "2015-09-17",
        "dateTo": "2015-09-17T13:00:00.000Z",
    }
    result = [
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
    assert requester.getDeployments(params) == result


def test_get_device(requester):
    params = {
        "deviceCode": "BPR-Folger-59",
        "dateFrom": "2005-09-17T00:00:00.000Z",
        "dateTo": "2020-09-17T13:00:00.000Z",
    }
    result = [
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

    result[0]["deviceLink"] = result[0]["deviceLink"].replace("data", "qa", 1)

    assert requester.getDevices(params) == result


def test_get_device_categories(requester):
    params = {
        "deviceCategoryCode": "CTD",
        "deviceCategoryName": "Conductivity",
        "description": "Temperature",
    }
    result = [
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
    assert requester.getDeviceCategories(params) == result


def test_get_properties(requester):
    params = {
        "propertyCode": "conductivity",
        "locationCode": "BACAX",
        "deviceCategoryCode": "CTD",
    }
    result = [
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

    assert requester.getProperties(params) == result


def test_get_data_products(requester):
    params = {
        "dataProductCode": "SHV",
    }
    result = [
        {
            "dataProductCode": "SHV",
            "dataProductName": "Spectrogram For Hydrophone Viewer",
            "dataProductOptions": [
                {
                    "allowableRange": {
                        "lowerBound": "-160.0",
                        "onlyIntegers": False,
                        "unitOfMeasure": None,
                        "upperBound": "140.0",
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
                        "lowerBound": "-160.0",
                        "onlyIntegers": False,
                        "unitOfMeasure": None,
                        "upperBound": "140.0",
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

    assert requester.getDataProducts(params) == result


def test_get_sensor_category_codes(requester):
    params = {
        "locationCode": "NCBC",
        "deviceCategoryCode": "BPR",
        "propertyCode": "seawatertemperature,totalpressure",
    }
    result = [
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
    assert requester.getSensorCategoryCodes(params) == result
