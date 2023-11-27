from time import sleep, time

import requests

from ._PollLog import _PollLog
from ._util import _printErrorMessage, saveAsFile
from .Exceptions import MaxRetriesException


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
            try:
                # Run timed request
                start = time()
                response = requests.get(self._baseUrl, self._filters, timeout=timeout)
                duration = time() - start

                self._downloadUrl = response.url
                self._status = response.status_code
                self._retries += 1

                # print('request got {:d}'.format(response.status_code))
                if maxRetries > 0 and self._retries > maxRetries:
                    raise MaxRetriesException(
                        f"   Maximum number of retries ({maxRetries}) exceeded"
                    )

                # Status 200: file downloaded
                # Status 202: processing
                # Status 204: no data
                # Status 400: error
                # Status 404: index out of bounds
                # Status 410: gone (file deleted from FTP)
                if self._status == 200:
                    # File downloaded, get filename from header and save
                    self._downloaded = True
                    self._downloadingTime = round(duration, 3)
                    filename = self.extractNameFromHeader(response)
                    self._filePath = filename
                    self._fileSize = len(response.content)
                    saved = saveAsFile(response, outPath, filename, overwrite)
                    if saved == 0:
                        pass
                    elif saved == -2:
                        if self._retries > 1:
                            print("")  # new line if required
                        print(f'   Skipping "{self._filePath}": File already exists.')
                        self._status = 777
                    else:
                        raise Exception(
                            f'An error ocurred when saving the file "{filename}"'
                        )

                elif self._status == 202:
                    # Still processing, wait and retry
                    log.logMessage(response.json())
                    sleep(pollPeriod)

                elif self._status == 204:
                    # No data found
                    print("   No data found.")

                elif self._status == 400:
                    # API Error
                    _printErrorMessage(response)
                    raise Exception(
                        f"The request failed with HTTP status {self._status}.",
                        response.json(),
                    )

                elif self._status == 404:
                    # Index too high, no more files to download
                    log.printNewLine()
                    pass

                else:
                    # Gone
                    print(
                        "   FTP Error: File not found. If the product order is recent,",
                        "retry downloading using the method downloadProduct",
                        f"with the runId: {self._filters['dpRunId']}",
                    )
                    _printErrorMessage(response)
            except Exception:
                raise

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
