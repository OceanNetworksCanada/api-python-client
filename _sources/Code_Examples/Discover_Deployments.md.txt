# Discover Deployments

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/deployments](https://data.oceannetworks.ca/OpenAPI#get-/deployments)

### Get all deployments for a specific device code

Return the deployments for the device with the _deviceCode_ "**NORTEKAQDPRO8398**".

```python
params = {
    "deviceCode": "NORTEKAQDPRO8398",
}
onc.getDeployments(params)
```

### Get all deployments at a specific location

Return all deployments at the location with the _locationCode_ "**BACAX**".

```python
params = {
    "locationCode": "BACAX",
}
onc.getDeployments(params)
```

### Get all deployments with a specific device category

Return all deployments with the _deviceCategoryCode_ "**ADCP2MHZ**".

```python
params = {
    "deviceCategoryCode": "ADCP2MHZ",
}
onc.getDeployments(params)
```

### Get all deployments with a specific property

Return all deployments with instruments that measure the property "**oxygen**".

```python
params = {
    "propertyCode": "oxygen",
}
onc.getDeployments(params)
```

### Get all deployments with a specific device category and a specific property

Return all deployments that have devices with the device category "**CTD**" and property "**pressure**".

```python
params = {
    "deviceCategoryCode": "CTD",
    "propertyCode": "pressure",
}
onc.getDeployments(params)
```

### Get all deployments between two dates

Return all deployments between 1 July 2010 and 30 June 2011.
Check [here](https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms#GlossaryofTerms-ISO8601Duration) for additional
information about the supported dates/times format.

```python
params = {
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getDeployments(params)
```

### Get all deployments at a specific location, between two dates

Return all deployments between 1 July 2010 and 30 June 2011, at the location with the _locationCode_ "**BACAX**" ("
Barkely Canyon Axis (POD1)").

```python
params = {
    "locationCode": "BACAX",
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getDeployments(params)
```

### Get all deployments at a specific location, between two dates, with a sensor with a specific property code

Return all deployments between 1 July 2010 and 30 June 2011, at the location with the _locationCode_ "**BACAX**" ("
Barkely Canyon Axis (POD1)"), with the _propertyCode_ "**seawatertemperature**".

```python
params = {
    "locationCode": "BACAX",
    "propertyCode": "seawatertemperature",
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getDeployments(params)
```
