# Discover Data Availability for Data Products

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/dataAvailability/dataproducts](https://data.oceannetworks.ca/OpenAPI#get-/dataAvailability/dataproducts)

### Get data availability from a specific location and a device category

Return which data products are available with _deviceCategoryCode_ "**BPR**" at location Barkley Upper Slope (
_locationCode_:"**NCBC**").

```python

params = {
    "deviceCategoryCode": "BPR",
    "locationCode": "NCBC",
}
onc.getDataAvailability(params)
```

### Get data availability from a specific device with a specific extension

Return which data products are available with _deviceCode_ "**BPR_BC**" and extension "**raw**"

```python

params = {
    "deviceCode": "BPR_BC",
    "extension": "raw",
}
onc.getDataAvailability(params)
```