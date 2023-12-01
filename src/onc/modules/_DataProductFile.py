from time import sleep, time
from warnings import warn

import requests

from ._PollLog import _PollLog
from ._util import _createErrorMessage, saveAsFile


class MaxRetriesException(RuntimeError):
    def __init__(self, max_retries):
        super().__init__(f"Maximum number of retries ({max_retries}) exceeded")


class _DataProductFile:
    """
    Donwloads a single data product file
    Is able to poll and wait if required
    """

    def __init__(self, dpRunId: int, index: str, baseUrl: str, token: str):
        self._retries = 0
        self._status = 202
        self._downloaded = False
        self._baseUrl = f"{baseUrl}api/dataProductDelivery"
        self._filePath = ""
        self._fileSize = 0
        self._runningTime = 0
        self._downloadingTime = 0

        self._filters = {
            "method": "download",
            "token": token,
            "dpRunId": dpRunId,
            "index": index,
        }
        # prepopulate download URL in case download() never happens
        self._downloadUrl = f"{self._baseUrl}?method=download&token={token}&dpRunId={dpRunId}&index={index}"  # noqa: E501

    def download(
        self,
        timeout: int,
        pollPeriod: float,
        outPath: str,
        maxRetries: int,
        overwrite: bool,
    ):
        """
        Download a file for the data product at runId
        Can poll, wait and retry if the file is not ready to download
        Return the file information
        """
        log = _PollLog(True)
        self._status = 202
        while self._status == 202:
            # Run timed request
            start = time()
            response = requests.get(self._baseUrl, self._filters, timeout=timeout)
            duration = time() - start

            self._downloadUrl = response.url
            self._status = response.status_code
            self._retries += 1

            if maxRetries > 0 and self._retries > maxRetries:
                raise MaxRetriesException(maxRetries)

            if self._status == 200:
                self._downloaded = True
                self._downloadingTime = round(duration, 3)
                filename = self.extractNameFromHeader(response)
                self._filePath = filename
                self._fileSize = len(response.content)
                try: 
                    saveAsFile(response, outPath, filename, overwrite)
                except FileExistsError:
                    if self._retries > 1:
                        print("")
                    print(f'   Skipping "{self._filePath}": File already exists.')
                    self._status = 777

            elif self._status == 202:  # Still processing, wait and retry
                log.logMessage(response.json())
                sleep(pollPeriod)

            elif self._status == 204:  # No data found
                print("   No data found.")

            elif self._status == 400:
                raise requests.HTTPError(_createErrorMessage(response))

            elif self._status == 404:  # Index too high, no more files to download
                log.printNewLine()
                pass

            elif self._status == 410:  # Status 410: gone (file deleted from FTP)
                warn(
                    "   FTP Error: File not found. If the product order is recent,",
                    "retry downloading using the method downloadProduct",
                    f"with the runId: {self._filters['dpRunId']}",
                )

        return self._status

    def extractNameFromHeader(self, response):
        """
        Returns the file name from the response.
        """
        txt = response.headers["Content-Disposition"]
        filename = txt.split("filename=")[1]
        return filename

    def setComplete(self):
        self._status = 200

    def getInfo(self):
        errorCodes = {
            "200": "complete",
            "202": "running",
            "204": "no content",
            "400": "error",
            "401": "unauthorized",
            "404": "not found",
            "410": "gone",
            "500": "server error",
            "777": "skipped",
        }

        txtStatus = errorCodes[str(self._status)]

        return {
            "url": self._downloadUrl,
            "status": txtStatus,
            "size": self._fileSize,
            "file": self._filePath,
            "index": self._filters["index"],
            "downloaded": self._downloaded,
            "requestCount": self._retries,
            "fileDownloadTime": float(self._downloadingTime),
        }
