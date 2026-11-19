# Discover Device Categories

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/deviceCategories](https://data.oceannetworks.ca/OpenAPI#get-/deviceCategories)

### Get all device categories

```python
onc.getDeviceCategories()
```

### Get the device category for a specific device category code

Return the device category information for the _deviceCategoryCode_ "**ADCP150KHZ**".

```python
params = {
    "deviceCategoryCode": "ADCP150KHZ",
}
onc.getDeviceCategories(params)
```

### Get all device categories which have a certain word in the name

Return all device categories which have "**acoustic**" in the name.

```python
params = {
    "deviceCategoryName": "acoustic",
}
onc.getDeviceCategories(params)
```

### Get all device categories which have a certain word in the description

Return all device categories which have "**doppler**" in the description.

```python
params = {
    "description": "doppler",
}
onc.getDeviceCategories(params)
```

### Get all device categories that are available at a specific location

Return all device categories that are available at the location with the _locationCode_ "**BACAX**" ("Barkley Canyon
Axis (POD1)").

```python
params = {
    "locationCode": "BACAX",
}
onc.getDeviceCategories(params)
```

### Get all the device categories which have devices that have a specific property

Return all device categories which have devices with the propertyCode "**salinity**".

```python
params = {
    "propertyCode": "salinity",
}
onc.getDeviceCategories(params)
```
