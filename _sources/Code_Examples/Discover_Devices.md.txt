# Discover Devices

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/devices](https://data.oceannetworks.ca/OpenAPI#get-/devices)

### Get all available devices

```python
onc.getDevices()
```

### Get the device information for a specific device code

Return the device with the _deviceCode_ "**NORTEKAQDPRO8398**".

```python
params = {
    "deviceCode": "NORTEKAQDPRO8398",
}
onc.getDevices(params)
```

### Get all devices which have a certain word in the device name

Return all devices with "**jasco**" in the name.

```python
params = {
    "deviceName": "jasco",
}
onc.getDevices(params)
```

### Get all devices that have been deployed at a specific location

Return all devices that have been deployed at the location with the _locationCode_ "**BACAX**".

```python
params = {
    "locationCode": "BACAX",
}
onc.getDevices(params)
```

### Get all devices from a specific device category

Return all devices with the _deviceCategoryCode_ "**ADCP2MHZ**".

```python
params = {
    "deviceCategoryCode": "ADCP2MHZ",
}
onc.getDevices(params)
```

### Get all devices with a specific property code

Return all devices that measures the propertyCode "**oxygen**".

```python
params = {
    "propertyCode": "oxygen",
}
onc.getDevices(params)
```

### Get all devices with a specific device category and a specific property code

Return all devices that has the device category "**CTD**" and property "**pressure**".

```python
params = {
    "deviceCategoryCode": "CTD",
    "propertyCode": "pressure",
}
onc.getDevices(params)
```

### Get all devices that support a specific data product code

Return all devices that support the dataProductCode "**IBPP**" ("Ice Buoy Profile Plots").

```python
params = {
    "dataProductCode": "IBPP",
}
onc.getDevices(params)
```

### Get all devices deployed between two dates

Return all devices deployed between 1 July 2010 and 30 June 2011.
Check [here](https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms#GlossaryofTerms-ISO8601Duration) for additional
information about the supported dates/times format.

```python
params = {
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getDevices(params)
```

### Get all devices deployed at a specific location, between two dates

Return all devices deployed between 1 July 2010 and 30 June 2011, at the location with the _locationCode_ "**BACAX**" ("
Barkely Canyon Axis (POD1)").

```python
params = {
    "locationCode": "BACAX",
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getDevices(params)
```

### Get all devices deployed at a specific location, between two dates, with a sensor of a specific property code

Return all devices deployed between 1 July 2010 and 30 June 2011, at the location with the _locationCode_ "**BACAX**" ("
Barkely Canyon Axis (POD1)"), with the _propertyCode_ "**seawatertemperature**".

```python
params = {
    "locationCode": "BACAX",
    "propertyCode": "seawatertemperature",
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getDevices(params)
```
