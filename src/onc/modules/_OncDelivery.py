from datetime import timedelta
from time import sleep, time
from warnings import warn

import humanize
import requests

from ._DataProductFile import _DataProductFile
from ._OncService import _OncService
from ._PollLog import _PollLog
from ._util import _createErrorMessage, _formatSize


class _OncDelivery(_OncService):
    """
    Methods that wrap the API data product delivery services
    """

    def __init__(self, parent: object, verbosity: str, redact_token: str, raise_http_errors: bool):
        super().__init__(parent, verbosity, redact_token, raise_http_errors)

        # Default seconds to wait between consecutive download tries of a file
        # (when no estimate processing time is available)
        self.pollPeriod = 2.0

    def orderDataProduct(
        self,
        filters: dict,
        maxRetries: int,
        downloadResultsOnly: bool,
        includeMetadataFile: bool,
        overwrite: bool,
    ):
        fileList = []
        # Request the product
        requestData = self.requestDataProduct(filters)

        if downloadResultsOnly:
            # Only run and return links
            runData = self.runDataProduct(requestData["dpRequestId"], waitComplete=True)
            for runId in runData["runIds"]:
                fileList.extend(
                    self._infoForProductFiles(
                        runId, runData["fileCount"], includeMetadataFile
                    )
                )
        else:
            # Run and download files
            runData = self.runDataProduct(
                requestData["dpRequestId"], waitComplete=False
            )
            for runId in runData["runIds"]:
                fileList.extend(
                    self._downloadProductFiles(
                        runId, includeMetadataFile, maxRetries, overwrite
                    )
                )

            print("")
            self._printProductOrderStats(fileList, runData)

        return self._formatResult(fileList, runData)

    def requestDataProduct(self, filters: dict):
        """
        Data product request
        """
        filters["method"] = "request"
        filters["token"] = self._config("token")
        url = "{:s}api/dataProductDelivery".format(self._config("baseUrl"))
        response = self._doRequest(url, filters)

        self._estimatePollPeriod(response)
        self._printProductRequest(response)
        return response

    def checkDataProduct(self, dpRequestId: int):
        url = f"{self._config('baseUrl')}api/dataProductDelivery/status"
        filters = {
            "dpRequestId": dpRequestId,
        }
        return self._doRequest(url, filters)

    def runDataProduct(self, dpRequestId: int, waitComplete: bool):
        """
        Run a product request.

        Optionally wait until the product generation is complete.
        Return a dictionary with information of the run process.
        """
        status = ""
        log = _PollLog(True)
        print(
            f"To cancel the running data product, run 'onc.cancelDataProduct({dpRequestId})'"  # noqa: E501
        )
        url = f"{self._config('baseUrl')}api/dataProductDelivery"
        runResult = {"runIds": [], "fileCount": 0, "runTime": 0, "requestCount": 0}

        start = time()
        while status != "complete":
            response = requests.get(
                url,
                {
                    "method": "run",
                    "token": self._config("token"),
                    "dpRequestId": dpRequestId,
                },
                timeout=self._config("timeout"),
            )
            code = response.status_code
            runResult["requestCount"] += 1

            if response.ok:
                data = response.json()
            else:
                raise requests.HTTPError(_createErrorMessage(response))

            if waitComplete:
                status = data[0]["status"]
                log.logMessage(data)
                if status == "cancelled":
                    break
                if code != 200:
                    sleep(self.pollPeriod)
            else:
                status = "complete"

        # self.print(data)
        # print('got filecount {}'.format(data[0]['fileCount']))
        runResult["fileCount"] = data[0]["fileCount"]
        runResult["runTime"] = time() - start

        # print a new line after the process finishes
        if waitComplete:
            print("")

        # gather a list of runIds
        for run in data:
            runResult["runIds"].append(run["dpRunId"])

        return runResult

    def cancelDataProduct(self, dpRequestId: int):
        url = f"{self._config('baseUrl')}api/dataProductDelivery/cancel"
        filters = {
            "dpRequestId": dpRequestId,
        }
        return self._doRequest(url, filters)

    def restartDataProduct(self, dpRequestId: int, waitComplete: bool):
        url = f"{self._config('baseUrl')}api/dataProductDelivery/restart"
        filters = {
            "dpRequestId": dpRequestId,
        }
        data = self._doRequest(url, filters)
        if waitComplete:
            return self.runDataProduct(dpRequestId, True)
        else:
            return data

    def downloadDataProduct(
        self,
        runId: int,
        maxRetries: int,
        downloadResultsOnly: bool,
        includeMetadataFile: bool,
        overwrite: bool,
    ):
        """
        Wrapper for downloadProductFiles that downloads data products with a runId.
        """
        if downloadResultsOnly:
            fileData = self._infoForProductFiles(runId, 0, includeMetadataFile)
        else:
            fileData = self._downloadProductFiles(
                runId, includeMetadataFile, maxRetries, overwrite
            )

        return fileData

    def _downloadProductFiles(
        self,
        runId: int,
        getMetadata: bool,
        maxRetries: int,
        overwrite: bool,
        fileCount: int = 0,
    ):
        fileList = []
        index = 1
        baseUrl = self._config("baseUrl")
        token = self._config("token")

        # keep increasing index until fileCount or until we get 404
        doLoop = True
        timeout = self._config("timeout")
        print(f"\nDownloading data product files with runId {runId}...")

        dpf = _DataProductFile(runId, str(index), baseUrl, token)

        # loop thorugh file indexes
        while doLoop:
            # stop after too many retries
            status = dpf.download(
                timeout,
                self.pollPeriod,
                self._config("outPath"),
                maxRetries,
                overwrite,
            )

            if status == 200 or status == 777:
                # file was downloaded (200), or skipped before downloading (777)
                fileList.append(dpf.getInfo())
                index += 1
                dpf = _DataProductFile(runId, str(index), baseUrl, token)

            elif status != 202 or (fileCount > 0 and index >= fileCount):
                # no more files to download
                doLoop = False

        # get metadata if required
        if getMetadata:
            dpf = _DataProductFile(runId, "meta", baseUrl, token)
            try:
                status = dpf.download(
                    timeout,
                    self.pollPeriod,
                    self._config("outPath"),
                    maxRetries,
                    overwrite,
                )
                if status == 200 or status == 777:
                    fileList.append(dpf.getInfo())
                    doLoop = False
            except Exception as ex:
                warn(
                    f"Metadata file not downloaded.  Reason: {type(ex)}" + str(ex),
                    RuntimeWarning,
                    stacklevel=2,
                )
                fileList.append(dpf.getInfo())

        return fileList

    def _infoForProductFiles(self, dpRunId: int, fileCount: int, getMetadata: bool):
        """
        Returns a list of information dictionaries for each file available for download.

        Returned rows will have the same structure as those returned by
        _DataProductFile.getInfo().
        """
        print(
            f"\nObtaining download information for data product files with runId {dpRunId}..."  # noqa: E501
        )

        # If we don't know the fileCount, get it from the server (takes longer)
        if fileCount <= 0:
            fileCount = self._countFilesInProduct(dpRunId)

        # Build a file list of data product file information
        fileList = []
        indexes = list(range(1, fileCount + 1))
        if getMetadata:
            indexes.append("meta")

        for index in indexes:
            dpf = _DataProductFile(
                dpRunId=dpRunId,
                index=str(index),
                baseUrl=self._config("baseUrl"),
                token=self._config("token"),
            )
            dpf.setComplete()
            fileList.append(dpf.getInfo())

        return fileList

    def _countFilesInProduct(self, runId: int):
        """
        Count the number of files available for download.

        Given a runId, polls the "download" method to count files.
        Uses HTTP HEAD to avoid downloading the files.
        """
        url = f"{self._config('baseUrl')}api/dataProductDelivery"
        filters = {
            "method": "download",
            "token": self._config("token"),
            "dpRunId": runId,
            "index": 1,
        }
        status = 200
        n = 0

        while status == 200 or status == 202:
            response = requests.head(
                url, params=filters, timeout=self._config("timeout")
            )
            status = response.status_code

            if status == 202:
                # If the file is still running, wait
                sleep(self.pollPeriod)
            elif status == 200:
                # count successful HEAD request
                filters["index"] += 1
                n += 1

        print(f"   {n} files available for download")
        return n

    def _printProductRequest(self, response):
        """
        Prints the information after a data product request.

        The request response format might differ depending on the
        product source (archive or generated on the fly).
        """
        isGenerated = "estimatedFileSize" in response
        print(f"Request Id: {response['dpRequestId']}")

        if isGenerated:
            size = response["estimatedFileSize"]  # API returns it as a formatted string
            print(f"Estimated File Size: {size}")
            if "estimatedProcessingTime" in response:
                print(
                    f"Estimated Processing Time: {response['estimatedProcessingTime']}"
                )
        else:
            size = _formatSize(response["fileSize"])
            print(f"File Size: {size}")
            print("Data product is ready for download.")

    def _estimatePollPeriod(self, response):
        """
        Parse estimated processing time and set polling.

        Sets a poll period adequate to the estimated processing time.
        Longer processing times require longer poll periods to
        avoid going over maxRetries.

        Does not work for archived data products because the response
        does not include estimatedProcessingTime.
        """
        if "estimatedProcessingTime" in response:
            txtEstimated = response["estimatedProcessingTime"]
            parts = txtEstimated.split(" ")
            if len(parts) == 2:
                unit = parts[1]
                factor = 1
                if unit == "min":
                    factor = 60
                elif unit == "hour":
                    factor = 3600
                total = factor * int(parts[0])
                self.pollPeriod = max(0.02 * total, 1.0)  # poll every 2%

                # set an upper limit to pollPeriod [sec]
                self.pollPeriod = min(self.pollPeriod, 10)

    def _printProductOrderStats(self, fileList: list, runInfo: dict):
        """
        Prints a formatted representation of the total time and size downloaded
        after the product order finishes
        """
        downloadCount = 0
        downloadTime = 0
        size = 0

        for file in fileList:
            size += file["size"]
            if file["downloaded"]:
                downloadCount += 1
                downloadTime += file["fileDownloadTime"]

        # Print run time
        runTime = timedelta(seconds=runInfo["runTime"])
        print(f"Total run time: {humanize.naturaldelta(runTime)}")

        if downloadCount > 0:
            # Print download time
            if downloadTime < 1.0:
                txtDownTime = f"{downloadTime:.3f} seconds"
            else:
                txtDownTime = humanize.naturaldelta(downloadTime)
            print(f"Total download Time: {txtDownTime}")

            # Print size and count of files
            natural_size = humanize.naturalsize(size, binary=True)
            print(f"{downloadCount} files ({natural_size}) downloaded")
        else:
            print("No files downloaded.")

    def _formatResult(self, fileList: list, runInfo: dict):
        size = 0
        downloadTime = 0
        requestCount = runInfo["requestCount"]

        for file in fileList:
            downloadTime += file["fileDownloadTime"]
            size += file["size"]
            requestCount += file["requestCount"]

        result = {
            "downloadResults": fileList,
            "stats": {
                "runTime": round(runInfo["runTime"], 3),
                "downloadTime": round(downloadTime, 3),
                "requestCount": requestCount,
                "totalSize": size,
            },
        }

        return result
