# Request (Near) Real-Time Data

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## [/scalardata/location](https://data.oceannetworks.ca/OpenAPI#get-/scalardata/location)

### Get the last scalar data reading available from a device in a location

```python
params = {
    "locationCode": "SEVIP",
    "deviceCategoryCode": "CTD",
    "rowLimit": "1",
    "getLatest": "true",
}

onc.getScalardata(params)

# Longer method name
# onc.getScalardataByLocation(params)

# Alias method name
# onc.getDirectByLocation(params)
```

### Get 1 minute of time-series scalar data readings from a a device in a location

```python
params = {
    "locationCode": "SEVIP",
    "deviceCategoryCode": "CTD",
    "dateFrom": "2016-09-01T00:00:00.000Z",
    "dateTo": "2016-09-01T00:01:00.000Z",
}

onc.getScalardata(params)

# Longer method name
# onc.getScalardataByLocation(params)

# Alias method name
# onc.getDirectByLocation(params)
```

### Get 10 seconds of raw CTD data readings from a location

```python
params = {
    "locationCode": "BACAX",
    "deviceCategoryCode": "CTD",
    "dateFrom": "2017-05-23T00:00:00.000Z",
    "dateTo": "2017-05-23T00:00:10.000Z",
}

onc.getRawdata(params)["data"]["readings"]

# Longer method name
# onc.getRawdataByLocation(params)["data"]["readings"]

# Alias method name
# onc.getDirectRawByLocation(params)["data"]["readings"]
```

## [/scalardata/device](https://data.oceannetworks.ca/OpenAPI#get-/scalardata/device)

### Get 10 seconds of raw data readings from a specific device

```python
params = {
    "deviceCode": "AMLMETRECX50348",
    "dateFrom": "2019-06-01T00:00:00.000Z",
    "dateTo": "2019-06-01T00:00:10.000Z",
}

onc.getRawdata(params)

# Longer method name
# onc.getRawdataByDevice(params)

# Alias method name
# onc.getDirectRawByDevice(params)
```

### Get 1 minute of time-series scalar data readings from a specific device

```python
params = {
    "deviceCode": "SBECTD19p4686",
    "dateFrom": "2016-09-01T00:00:00.000Z",
    "dateTo": "2016-09-01T00:01:00.000Z",
}

onc.getScalardata(params)

# Longer method name
# onc.getScalardataByDevice(params)

# Alias method name
# onc.getDirectByDevice(params)
```
