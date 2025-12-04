# Download Data Products

```python
# Get the token from your Oceans 3.0 profile page
from onc import ONC

onc = ONC("YOUR_TOKEN")
```

## Request, run, and download a data product

### Download a time-series data plot with file extension _png_ from a CTD located at Straight of Georgia East

```python
params = {
    "locationCode": "SEVIP",
    "deviceCategoryCode": "CTD",
    "dataProductCode": "TSSP",
    "extension": "png",
    "dateFrom": "2019-06-20T00:00:00.000Z",
    "dateTo": "2019-06-21T00:00:00.000Z",
    "dpo_qualityControl": "1",
    "dpo_resample": "none",
}
result = onc.orderDataProduct(params, includeMetadataFile=False)
```

### Download _csv_ files of time series scalar data readings from amn ADCP device located at Barkley Canyon Axis

```python
params = {
    "locationCode": "BACAX",
    "deviceCategoryCode": "ADCP2MHZ",
    "dataProductCode": "TSSD",
    "extension": "csv",
    "dateFrom": "2016-07-27T00:00:00.000Z",
    "dateTo": "2016-08-01T00:00:00.000Z",
    "dpo_qualityControl": 1,
    "dpo_resample": "none",
    "dpo_dataGaps": 0,
}
result = onc.orderDataProduct(params)
```
