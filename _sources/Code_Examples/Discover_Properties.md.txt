# Discover Properties

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/properties](https://data.oceannetworks.ca/OpenAPI#get-/properties)

### Get all properties

```python
onc.getProperties()
```

### Get the property information for a specific property code

Return the property for the _propertyCode_ "**seawatertemperature**".

```python
params = {
    "propertyCode": "seawatertemperature",
}
onc.getProperties(params)
```

### Get all properties which have a certain word in the property name

Return all properties which have "**pressure**" in the name.

```python
params = {
    "propertyName": "pressure",
}
onc.getProperties(params)
```

### Get all of the properties that are available at a specific location

Return all properties that are available at the location with the _locationCode_ "**BACAX**" ("Barkley Canyon Axis (
POD1)").

```python
params = {
    "locationCode": "BACAX",
}
onc.getProperties(params)
```

### Get all properties that are available for specific device

Return all properties available for a device with the _deviceCode_ "**NORTEKAQDPRO8398**".

```python
params = {
    "deviceCode": "NORTEKAQDPRO8398",
}
onc.getProperties(params)
```

### Get all properties that are available for a specific device category

Return all properties which are available for the device category "**ADCP150KHZ**".

```python
params = {
    "deviceCategoryCode": "ADCP150KHZ",
}
onc.getDeviceCategories(params)
```
