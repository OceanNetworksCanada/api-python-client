# Changelog

## v2.5.1 (2025-07-12)

### Enhancements

- Change the default value of `showWarning` to be `False`.

### Fixes

- Ignore timezone when parsing non-standard datetime like "YYYY-MM-DD".
  ([#60](https://github.com/OceanNetworksCanada/api-python-client/issues/60))

### Contributors

- [Kan Fu](https://github.com/kan-fu)

## v2.5.0 (2025-02-13)

### Enhancements

- Added `getArchivefileUrl` and `getArchivefileUrls` to only return the download links of
  the requested archive files.
  ([#56](https://github.com/OceanNetworksCanada/api-python-client/issues/56))

  This is useful because users can use them in their favorite download manager.
  Check the [Code Example](https://oceannetworkscanada.github.io/api-python-client/Code_Examples/Download_Archived_Files.html#download-archived-files-using-a-download-manager)
  for more information.

- Added warning messages if the response has a "messages" key with a non-empty list value.
  ([#58](https://github.com/OceanNetworksCanada/api-python-client/pull/58))

  This feature can be turned off by using `onc = ONC(token=TOKEN, showWarning=False)`.

### Fixes

- Reverted back the incremental downloading files because it might generate invalid files
  with partial file size (before it was zero file size).
  ([#54](https://github.com/OceanNetworksCanada/api-python-client/issues/54))

### Contributors

- [Kan Fu](https://github.com/kan-fu)

### Reviewers panel

- [Angela Schlesinger](https://github.com/aschlesin)
- [Eli Ferguson](https://github.com/eliferguson)
- [Spencer Plovie](https://github.com/spencerwplovie)

## v2.4.1 (2024-09-24)

### Fixes

- Fixed duplicate downloading issues when the downloaded file exists and the overwrite parameter is False
  in `downloadArchivefile`, `downloadDataProduct`, and `orderDataProduct`.
  ([#41](https://github.com/OceanNetworksCanada/api-python-client/issues/41))

- Fixed incorrect time estimation when downloading scalardata in multiple pages.
  ([#45](https://github.com/OceanNetworksCanada/api-python-client/issues/45))

### Contributors

- [Kan Fu](https://github.com/kan-fu)

### Reviewers panel

- [Angela Schlesinger](https://github.com/aschlesin)
- [Eli Ferguson](https://github.com/eliferguson)

## v2.4.0 (2024-05-30)

### Enhancements

- Improved package setup (pyproject.toml, linting and formatter).
  ([#1](https://github.com/OceanNetworksCanada/api-python-client/issues/1))

  Now you can import the ONC class using `from onc import ONC` instead of `from onc.onc import ONC`.
  The longer version still works.

- Added support of Path type for outPath (instance variable in ONC class).
  ([#12](https://github.com/OceanNetworksCanada/api-python-client/issues/12))
- Added GitHub Actions for continuous integration.
  ([#19](https://github.com/OceanNetworksCanada/api-python-client/issues/19))
- Added Sphinx for generating documentation.
  ([#7](https://github.com/OceanNetworksCanada/api-python-client/issues/7))
- Improved exception types raised and caught.
  ([#17](https://github.com/OceanNetworksCanada/api-python-client/issues/17))
- Added new public methods (`checkDataProduct`, `cancelDataProduct`, `restartDataProduct`, `getSensorCategoryCodes`) to match backend API update.
  ([#26](https://github.com/OceanNetworksCanada/api-python-client/issues/26))
- Renamed some public methods (old names are still available) to make the naming more consistent with the api end points.
  ([#33](https://github.com/OceanNetworksCanada/api-python-client/issues/33))

  | API End Point         | Old Name               | New Name                  |
  | --------------------- | ---------------------- | ------------------------- |
  | /locations/tree       | getLocationHierarchy   | getLocationsTree          |
  | /scalardata/location  | getDirectByLocation    | getScalardataByLocation   |
  | /scalardata/device    | getDirectByDevice      | getScalardataByDevice     |
  | /rawdata/location     | getDirectRawByLocation | getRawdataByLocation      |
  | /rawdata/device       | getDirectRawByDevice   | getRawdataByDevice        |
  | /archivefile/location | getListByLocation      | getArchivefileByLocation  |
  | /archivefile/device   | getListByDevice        | getArchivefileByDevice    |
  | /archivefile/download | getFile                | downloadArchivefile       |
  | N/A                   | getDirectFiles         | downloadDirectArchivefile |

- Added helper methods to combine `getXXXByLocation` and `getXXXByDevice` into `getXXX`.
  ([#33](https://github.com/OceanNetworksCanada/api-python-client/issues/33))

  Namely, `getScalardata`, `getRawdata` and `getArchivefile`.

### Fixes

- Removed unused modules (onc/ags.py, onc/dap.py, onc/nerc.py, onc/sos.py).
  ([#1](https://github.com/OceanNetworksCanada/api-python-client/issues/1))

### Tests

- Added support using .env file for storing the token when running tests.
  ([#2](https://github.com/OceanNetworksCanada/api-python-client/issues/2))
- Replaced robot framework with pytest.
  ([#10](https://github.com/OceanNetworksCanada/api-python-client/issues/10))

### Contributors

- [Jacob Stevens-Haas](https://github.com/Jacob-Stevens-Haas)
- [Kan Fu](https://github.com/kan-fu)
- [Renfu Li](https://github.com/Renfu-Li)

### Reviewers panel

- [Angela Schlesinger](https://github.com/aschlesin)
- [Eli Ferguson](https://github.com/eliferguson)
- [Jacob Stevens-Haas](https://github.com/Jacob-Stevens-Haas)
- [Spencer Plovie](https://github.com/spencerwplovie)

## v2.3.5 (2019-12-12) and before

### Contributors

- [Dany Alejandro Cabrera](https://github.com/danyalejandro)
