import numpy as np
import pandas as pd
import xarray as xr

from .util import FlagTerm


def nan_onc_flags(ds: xr.Dataset, flags_to_nan: list[int] = [4]) -> xr.Dataset:
    """
    Set corresponding data values to NaN if the flag is in flags_to_nan.

    Parameters
    ----------
    ds: xr.Dataset
        The input xarray Dataset. The dataset must contain data variables and matching
        flag variables prepended with FlagTerm (defined in util.util).
    flags_to_nan: list[int]
        A list of integer flag values to set to NaN if they are present in a variable.
        By default, only the flag for bad data (4) is supplied.

    Returns
    -------
    xr.Dataset

    Examples
    ----------
    >>> data = nan_onc_flags(data, flags_to_nan = [3,4]) # doctest: +SKIP
    """

    flag_vars = [v for v in ds.data_vars if v.startswith(FlagTerm)]
    if len(flag_vars) != 0:
        for fv in flag_vars:
            dv = fv.replace(FlagTerm + '_', '')
            if dv in ds.data_vars:
                ds[dv] = ds[dv].where(~ds[fv].isin([flags_to_nan]), np.nan)
    return ds


def remove_onc_flag_vars(ds: xr.Dataset) -> xr.Dataset:
    """
    Remove all flag variables from an xarray Dataset.
    Usually this can be implemented after using nan_onc_flags to set bad data to NaN,
    or if you don't care about the flag output.

    Parameters
    ----------
    ds: xr.Dataset
        The input xarray Dataset.

    Returns
    -------
    xr.Dataset

    Examples
    ----------
    >>> data = remove_onc_flag_vars(data) # doctest: +SKIP
    """

    flag_vars = [v for v in ds.data_vars if v.startswith(FlagTerm)]
    if len(flag_vars) != 0:
        ds = ds.drop_vars(flag_vars, errors='ignore')
    return ds


def json2xarray(json_response_data: dict, join_method: str = 'outer') -> xr.Dataset:
    """
    Convert a getScalarData JSON response to an xarray Dataset.
    This function only supports use of 'array' outputFormat and 'full' metadata
    query parameters.

    Parameters
    ----------
    json_response_data: dict
        A json object returned from an ONC getScalarData request.
    join_method: str
        The method to combine variables on. Options are the same as
        xr.combine_by_coords join options.

    Returns
    -------
    xr.Dataset

    Examples
    ----------
    >>> data = json2xarray(json_response_data) # doctest: +SKIP
    """

    # Light checks because this function only handles certain conditions.
    if json_response_data['parameters']['outputFormat'].lower() != 'array':
        raise NotImplementedError("Only 'array' outputFormat is currently supported.")
    elif json_response_data['parameters']['metaData'].lower() != 'full':
        raise NotImplementedError("Only 'full' metadata is currently supported.")

    loc_code = json_response_data['parameters']['locationCode'].upper()

    cit = json_response_data['citations']
    doi_info = [c['citations'] for c in cit] if len(cit) > 1 else cit[0]['citation']

    metadata = json_response_data['metadata']
    depth = metadata['depth']
    dev_cat_code = metadata['deviceCategoryCode']
    loc_name = metadata['locationName']

    qaqc_flag_info = '\n'.join([f"{k}:{v}" for k, v in
                                json_response_data['qaqcFlagInfo'].items()])

    device_data = json_response_data['sensorData']

    vds_list = []
    for var_data in device_data:  # This could probably be parallelized in the future.

        # The sensorName is more descriptive than the propertyCode.
        var_name = var_data['sensorName'].replace(' ', '_')
        var_name = var_name.replace('-', '_')
        var_name = var_name.replace('(', '')
        var_name = var_name.replace(')', '')
        var_name = var_name.lower()

        flag_var_name = f"{FlagTerm}_{var_name}"

        var_times = var_data['data']['sampleTimes']
        var_values = var_data['data']['values']
        var_flags = var_data['data']['qaqcFlags']

        vds = xr.Dataset()
        vds = vds.assign_coords({'time': pd.to_datetime(var_times).tz_localize(None)})
        vds[var_name] = (('time'), var_values)
        vds[flag_var_name] = (('time'), var_flags)

        # Fill any potential NaNs with a flag indicating no QAQC performed (0).
        vds[flag_var_name] = vds[flag_var_name].fillna(0)

        # Convert time dtypes to reduce object size.
        vds['time'] = vds['time'].astype('datetime64[ms]')
        vds[flag_var_name] = vds[flag_var_name].astype('int8')

        # Assign variable level attributes.
        vds[var_name].attrs['units'] = var_data['unitOfMeasure']
        vds[var_name].attrs['long_name'] = var_data['sensorName']
        vds[var_name].attrs['propertyCode'] = var_data['propertyCode']
        vds[var_name].attrs['sensorCategoryCode'] = var_data['sensorCategoryCode']
        vds[var_name].attrs['sensorName'] = var_data['sensorName']
        vds[var_name].attrs['sensorCode'] = var_data['sensorCode']
        vds[var_name].attrs['deviceCategoryCode'] = dev_cat_code

        vds[flag_var_name].attrs['variable'] = var_name
        vds[flag_var_name].attrs['qaqcFlagInfo'] = qaqc_flag_info

        vds['time'].attrs['timezone'] = 'UTC'

        vds_list.append(vds)

    ds = xr.combine_by_coords(vds_list, join=join_method)
    ds = ds[sorted(ds.data_vars)]

    # Assign root level attributes.
    ds.attrs['locationCode'] = loc_code
    ds.attrs['locationName'] = loc_name
    ds.attrs['deviceCategoryCode'] = dev_cat_code
    ds.attrs['citations'] = doi_info
    ds.attrs['qaqcFlagInfo'] = qaqc_flag_info
    if 'depth' not in ds.data_vars:
        ds.attrs['depth'] = depth
    return ds
