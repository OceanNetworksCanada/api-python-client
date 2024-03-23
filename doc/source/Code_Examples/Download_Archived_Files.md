# Download Archived Files

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/archivefile/device](https://data.oceannetworks.ca/OpenAPI#get-/archivefile/device)

### Get a list of all archived files available from a specific device for a specific time-range

Return the archived files for a device with _deviceCode_ "**RDIADCP600WH25471**"

```python
params = {
    "deviceCode": "RDIADCP600WH25471",
    "dateFrom": "2019-06-07T00:00:00.000Z",
    "dateTo": "2019-06-08T00:00:00.000Z",
}

onc.getListByDevice(params)
```

### Get a list of all archived files available from a specific device for a specific time-range with a specific extension

Return the archived files for an ADCP instrument with _deviceCode_ "**RDIADCP600WH25471**" that have _rdi_ as the
extension name.

```python
params = {
    "deviceCode": "RDIADCP600WH25471",
    "extension": "rdi",
    "dateFrom": "2019-06-07T00:00:00.000Z",
    "dateTo": "2019-06-08T00:00:00.000Z",
}

onc.getListByDevice(params)
```

### Download a file by its filename

```python
onc.getFile("RDIADCP600WH25471_20190607T120000.555Z.rdi", overwrite=True)
```

## [/archivefile/location](https://data.oceannetworks.ca/OpenAPI#get-/archivefile/location)

### Get a list of all archived files available from a specific location and a device category for a specific time-range

Return the archived files for a device with _deviceCategoryCode_ "**HYDROPHONE**" at location Straight of Georgia East (
_locationCode_:"**SEVIP**")

```python
params = {
    "deviceCategoryCode": "HYDROPHONE",
    "locationCode": "SEVIP",
    "dateFrom": "2017-01-01T00:00:00.000Z",
    "dateTo": "2019-12-31T00:00:00.000Z",
}

onc.getListByLocation(params)["files"]
```

### Get a list of all archived files available from a specific location and a device category for a specific time-range with a specific file extension

Return the archived files for a device with _deviceCategoryCode_ "**HYDROPHONE**" at location Straight of Georgia East (
_locationCode_:"**SEVIP**") with file extension "**wav**".

```python
params = {
    "deviceCategoryCode": "HYDROPHONE",
    "locationCode": "SEVIP",
    "extension": "wav",
    "dateFrom": "2017-01-01T00:00:00.000Z",
    "dateTo": "2019-12-31T00:00:00.000Z",
}

onc.getListByLocation(params)["files"]
```

## Download archived files that match the parameters

Download all "wav" files from a hydrophone at Straight of Georgia East (_locationCode_:"**SEVIP**") from the last 2
hours

```python
import datetime

# Get the current ISO8601 timestamp, without milliseconds
now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + ".000Z"

params = {
    "locationCode": "SEVIP",  # Strait of Georgia East
    "deviceCategoryCode": "HYDROPHONE",  # Hydrophones
    "dateFrom": "-PT2H",  # Minus 2 hours from dateTo
    "dateTo": now,
    "extension": "wav",
}

# Download available files (will throw an exception if there are no deployments for the device during the last two hours)
# onc.getDirectFiles(params)
```
