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

onc.getArchivefile(params)

# Longer method name
# onc.getArchivefileByDevice(params)

# Alias method name
# onc.getListByDevice(params)
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

onc.getArchivefile(params)

# Longer method name
# onc.getArchivefileByDevice(params)

# Alias method name
# onc.getListByDevice(params)
```

### Download a file by its filename

```python

onc.downloadArchivefile("ICLISTENHF1560_20181005T000403.000Z-spect.mat", overwrite=True)

# Alias method name
# onc.getFile("ICLISTENHF1560_20181005T000403.000Z-spect.mat", overwrite=True)
```

## [/archivefile/location](https://data.oceannetworks.ca/OpenAPI#get-/archivefile/location)

### Get a list of all archived files available from a specific location and a device category for a specific time-range

Return the archived files for a device with _deviceCategoryCode_ "**HYDROPHONE**" at location Straight of Georgia East (
_locationCode_:"**SEVIP**")

```python
params = {
    "deviceCategoryCode": "HYDROPHONE",
    "locationCode": "SEVIP",
    "dateFrom": "2018-10-05T00:05:00.000Z",
    "dateTo": "2018-10-05T00:06:00.000Z",
}

onc.getArchivefile(params)

# Longer method name
# onc.getArchivefileByLocation(params)

# Alias method name
# onc.getListByLocation(params)
```

### Get a list of all archived files available from a specific location and a device category for a specific time-range with a specific file extension

Return the archived files for a device with _deviceCategoryCode_ "**HYDROPHONE**" at location Straight of Georgia East (
_locationCode_:"**SEVIP**") with file extension "**mat**".

```python
params = {
    "deviceCategoryCode": "HYDROPHONE",
    "locationCode": "SEVIP",
    "extension": "mat",
    "dateFrom": "2018-10-05T00:05:00.000Z",
    "dateTo": "2018-10-05T00:06:00.000Z",
}

onc.getArchivefile(params)

# Longer method name
# onc.getArchivefileByLocation(params)

# Alias method name
# onc.getListByLocation(params)
```

## Download archived files that match the parameters

Download all "mat" files from a hydrophone at Straight of Georgia East (_locationCode_:"**SEVIP**") using the parameter above.

```python
params = {
    "deviceCategoryCode": "HYDROPHONE",
    "locationCode": "SEVIP",
    "extension": "mat",
    "dateFrom": "2018-10-05T00:05:00.000Z",
    "dateTo": "2018-10-05T00:06:00.000Z",
}

onc.downloadDirectArchivefile(params)

# Alias method name
# onc.getDirectFiles(params)

```
