# Discover Data Products

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/dataProducts](https://data.oceannetworks.ca/OpenAPI#get-/dataProducts)

### Get all data products and their individual parameters from Oceans 3.0

```python
onc.getDataProducts()
```

### Get the data product options that are available for a specific data product code

Return all data product options for the _dataProductCode_ "**TSSD**" ("Time Series Scalar Data").

```python
params = {
    "dataProductCode": "TSSD",
}
onc.getDataProducts(params)
```

### Get all data product options that are available with a specific file extension

Return all data product options which are available for the _extension_ "**pdf**".

```python
params = {
    "extension": "pdf",
}
onc.getDataProducts(params)
```

### Get all data product options available for a specific data product code and specific file extension

Return all data product options which are available for the _dataProductCode_ "**TSSD**" and _extension_ "**csv**".

```python
params = {
    "dataProductCode": "TSSD",
    "extension": "csv",
}
onc.getDataProducts(params)
```

### Get all data product options which have a certain word in the data product name

Return all data product options which have "**scalar**" in the name.

```python
params = {
    "dataProductName": "scalar",
}
onc.getDataProducts(params)
```

### Get all data product options that are available at a specific location on ONCs network

Return all data product options that are available at the location with the _locationCode_ "**BACAX**" ("Barkley Canyon
Axis (POD1)").

```python
params = {
    "locationCode": "BACAX",
}
onc.getDataProducts(params)
```

### Get all data product options that are available for a specific file extension at a specific locationCode

Return all data product options that are available for the _extension_ "**mat**" at the location with the
_locationCode_ "**BACAX**" ("Barkley Canyon Axis (POD1)").

```python
params = {
    "extension": "mat",
    "locationCode": "BACAX",
}
onc.getDataProducts(params)
```

### Get all data products and their filter parameter options that are available on a specific deployed device

Return all data product codes available for a device with the _deviceCode_ "**NORTEKAQDPRO8398**".

```python
params = {
    "deviceCode": "NORTEKAQDPRO8398",
}
onc.getDataProducts(params)
```

### Get all data product options that are available for a specific device category

Return all data product options which are available for the _deviceCategoryCode_ "**ADCP150KHZ**".

```python
params = {
    "deviceCategoryCode": "ADCP150KHZ",
}
onc.getDataProducts(params)
```
