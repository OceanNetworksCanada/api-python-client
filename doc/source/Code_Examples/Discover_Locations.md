# Discover Locations

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/locations](https://data.oceannetworks.ca/OpenAPI#get-/locations)

### Get all locations

```python
onc.getLocations()
```

### Get the location for a specific location code

Return the location with the _locationCode_ "**BACAX**".

```python
params = {
    "locationCode": "BACAX",
}
onc.getLocations(params)
```

### Get all locations, including and underneath a location in the Oceans 3.0 Data Search Tree

Return all locations including and below location Northeast Pacific (locationCode:"**NEP**") in the Oceans
3.0 [Data Search Tree](https://data.oceannetworks.ca/DataSearch?locationCode=NEP).

```python
params = {
    "locationCode": "NEP",
    "includeChildren": "true",
}
onc.getLocations(params)
```

### Get all locations with instruments of a specific device category, including and below a location in the Oceans 3.0 Data Search Tree

Return all locations in Northeast Pacific (locationCode:"**NEP**") with hydrophones deployed.

```python
params = {
    "locationCode": "NEP",
    "deviceCategoryCode": "HYDROPHONE",
    "includeChildren": "true",
}
onc.getLocations(params)
```

### Get all locations which have a certain word in the location name

Return all locations with "**underwater**" as part of the name.

```python
params = {
    "locationName": "underwater",
}
onc.getLocations(params)
```

### Get all locations with instruments from a specific device category

Return all locations which have at least one instrument for the _deviceCategoryCode_ "**ADCP150KHZ**".

```python
params = {
    "deviceCategoryCode": "ADCP150KHZ",
}
onc.getLocations(params)
```

### Get all locations with instruments that have a specific property code

Return all locations that have instruments that measures the property "**totalpressure**".

```python
params = {
    "propertyCode": "totalpressure",
}
onc.getLocations(params)
```

### Get all locations with instruments that have a specific device category and a specific property

Return all locations with at least one instrument that has the device category "**BPR**" and property code "*
*totalpressure**".

```python
params = {
    "deviceCategoryCode": "BPR",
    "propertyCode": "pressure",
}
onc.getLocations(params)
```

### Get all locations where a specific device has been deployed

Return all locations where a device with the unique _deviceCode_ "**NORTEKAQDPRO8398**" has been deployed.

```python
params = {
    "deviceCode": "NORTEKAQDPRO8398",
}
onc.getLocations(params)
```

### Get all locations with instruments that support a specific data product code

Return all Locations with instruments that support the _dataProductCode_ "**IBPP**" ("Ice Buoy Profile Plots").

```python
params = {
    "dataProductCode": "IBPP",
}
onc.getLocations(params)
```

### Get all locations with instruments deployed between two dates

Return all locations with instruments that were deployed between 1 July 2010 and 30 June 2011.
Check [here](https://wiki.oceannetworks.ca/display/O2A/Glossary+of+Terms#GlossaryofTerms-ISO8601Duration) for additional
information about the supported dates/times format.

```python
params = {
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getLocations(params)
```

### Get all locations with instruments deployed between two dates, with a sensor for a specific property

Return all locations with instruments that were deployed between 1 July 2010 and 30 June 2011, and have a sensor for the
_propertyCode_ "**seawatertemperature**".

```python
params = {
    "propertyCode": "seawatertemperature",
    "dateFrom": "2010-07-01",
    "dateTo": "2011-06-30T23:59:59.999Z",
}
onc.getLocations(params)
```

## [/locations/tree](https://data.oceannetworks.ca/OpenAPI#get-/locations/tree)

### Get location hierarchy including and below a specific location

Return the location hierarchy from the "**MOBP**" ("Mobile Platforms") node and below.

```python
params = {
    "locationCode": "MOBP",
}
onc.getLocationHierarchy(params)
```
