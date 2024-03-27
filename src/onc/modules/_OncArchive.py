import os
import time
from pathlib import Path

import humanize
import requests

from ._MultiPage import _MultiPage
from ._OncService import _OncService
from ._util import _createErrorMessage, _formatDuration, saveAsFile


class _OncArchive(_OncService):
    """
    Methods that wrap the API archivefiles service
    """

    def __init__(self, parent: object):
        super().__init__(parent)

    def getArchivefileByLocation(self, filters: dict, allPages: bool):
        """
        Return a list of archived files for a device category in a location.

        The filenames obtained can be used to download files using the getFile() method.
        """
        return self._getList(filters, by="location", allPages=allPages)

    def getArchivefileByDevice(self, filters: dict, allPages: bool):
        """
        Return a list of archived files from a specific device.

        The filenames obtained can be used to download files using the getFile() method.
        """
        return self._getList(filters, by="device", allPages=allPages)

    def getArchivefile(self, filters: dict, allPages: bool):
        return self._delegateByFilters(
            byDevice=self.getArchivefileByDevice,
            byLocation=self.getArchivefileByLocation,
            filters=filters,
            allPages=allPages,
        )

    def downloadArchivefile(self, filename: str = "", overwrite: bool = False):
        url = self._serviceUrl("archivefiles")

        filters = {
            "token": self._config("token"),
            "method": "getFile",
            "filename": filename,
        }

        # Download the archived file with filename (response contents is binary)
        start = time.time()
        response = requests.get(url, filters, timeout=self._config("timeout"))
        status = response.status_code
        elapsed = time.time() - start

        if response.ok:
            # Save file to output path
            outPath: Path = self._config("outPath")
            saveAsFile(response, outPath, filename, overwrite)

        else:
            msg = _createErrorMessage(response)
            raise requests.HTTPError(msg)

        # Prepare a readable status
        txtStatus = "error"
        if status == 200:
            txtStatus = "completed"

        return {
            "url": response.url,
            "status": txtStatus,
            "size": len(response.content),
            "downloadTime": round(elapsed, 3),
            "file": filename,
        }

    def downloadDirectArchivefile(
        self, filters: dict, overwrite: bool = False, allPages: bool = False
    ):
        """
        Download a list of archived files that match the filters provided.

        This function invokes the method getListByLocation() or getListByDevice()
        to obtain a list of files, and the method getFile() to download all files found.

        See https://wiki.oceannetworks.ca/display/O2A/archivefiles
        for usage and available filters.
        """
        # make sure we only get a simple list of files
        if "returnOptions" in filters:
            del filters["returnOptions"]

        # Get a list of files
        dataRows = self.getArchivefile(filters, allPages)

        n = len(dataRows["files"])
        print(f"Obtained a list of {n} files to download.")

        # Download the files obtained
        tries = 1
        successes = 0
        size = 0
        time = 0
        downInfos = []
        for filename in dataRows["files"]:
            # only download if file doesn't exist (or overwrite is True)
            outPath: Path = self._config("outPath")
            filePath = outPath / filename
            fileExists = os.path.exists(filePath)

            if (not fileExists) or (fileExists and overwrite):
                print(f'   ({tries} of {n}) Downloading file: "{filename}"')
                downInfo = self.downloadArchivefile(filename, overwrite)
                size += downInfo["size"]
                time += downInfo["downloadTime"]
                downInfos.append(downInfo)
                successes += 1
                tries += 1
            else:
                print(f'   Skipping "{filename}": File already exists.')
                downInfo = {
                    "url": self._getDownloadUrl(filename),
                    "status": "skipped",
                    "size": 0,
                    "downloadTime": 0,
                    "file": filename,
                }
                downInfos.append(downInfo)

        print(f"{successes} files ({humanize.naturalsize(size)}) downloaded")
        print(f"Total Download Time: {_formatDuration(time)}")

        return {
            "downloadResults": downInfos,
            "stats": {"totalSize": size, "downloadTime": time, "fileCount": successes},
        }

    def _getDownloadUrl(self, filename: str):
        """
        Returns an archivefile absolute download URL for a filename
        """
        url = self._serviceUrl("archivefiles")
        return "{:s}?method=getFile&filename={:s}&token={:s}".format(
            url, filename, self._config("token")
        )

    def _getList(self, filters: dict, by: str = "location", allPages: bool = False):
        """
        Wraps archivefiles getListByLocation and getListByDevice methods
        """
        url = self._serviceUrl("archivefiles")
        filters["token"] = self._config("token")
        filters["method"] = (
            "getListByLocation" if by == "location" else "getListByDevice"
        )

        # parse and remove the artificial parameter extension
        extension = None
        filters2 = filters.copy()
        if "extension" in filters2:
            extension = filters2["extension"]

        if allPages:
            mp = _MultiPage(self)
            result = mp.getAllPages("archivefiles", url, filters2)
        else:
            if "extension" in filters2:
                del filters2["extension"]
            result = self._doRequest(url, filters2)
            result = self._filterByExtension(result, extension)
        return result

    def _filterByExtension(self, results: dict, extension: str):
        """
        Filter results to only those where filenames end with the extension
        If extension is None, won't do anything
        Returns the filtered list
        """
        if extension is None:
            return results

        extension = "." + extension  # match the dot to avoid matching substrings
        n = len(extension)
        filtered = []  # appending is faster than deleting

        # determine the row structure
        rowFormat = "filename"
        if len(results["files"]) > 0 and isinstance(results["files"][0], dict):
            rowFormat = "dict"

        # filter
        for file in results["files"]:
            if rowFormat == "filename":
                if file[-n:] == extension:
                    filtered.append(file)
            else:
                if file["filename"][-n:] == extension:
                    filtered.append(file)
        results["files"] = filtered

        return results
