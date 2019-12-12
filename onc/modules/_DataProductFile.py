import requests
import os
from time import sleep, time
from .Exceptions import MaxRetriesException
from ._util import saveAsFile
from ._util import _printErrorMessage
from ._PollLog import _PollLog

class _DataProductFile:
    """
    Donwloads a single data product file
    Is able to poll and wait if required
    """

    def __init__(self, dpRunId: int, index: str, baseUrl: str, token: str):
        self._retries     = 0
        self._status      = 202
        self._downloaded  = False
        self._baseUrl     = '{:s}api/dataProductDelivery'.format(baseUrl)
        self._filePath    = ''
        self._fileSize    = 0
        self._runningTime = 0
        self._downloadingTime = 0

        self._filters = {
            'method' : 'download',
            'token'  : token,
            'dpRunId': dpRunId,
            'index'  : index
        }
        # prepopulate download URL in case download() never happens
        self._downloadUrl = '{:s}?method=download&token={:s}&dpRunId={:d}&index={:s}'.format(baseUrl, token, dpRunId, index)

    
    def download(self, timeout: int, pollPeriod: float, outPath: str, maxRetries: int, overwrite: bool):
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
                
                #print('request got {:d}'.format(response.status_code))
                if maxRetries > 0 and self._retries > maxRetries:
                    raise MaxRetriesException('   Maximum number of retries ({:d}) exceeded'.format(maxRetries))
                
                # Status 200: file downloaded, 202: processing, 204: no data, 400: error, 404: index out of bounds, 410: gone (file deleted from FTP) 
                if self._status == 200:
                    # File downloaded, get filename from header and save
                    self._downloaded = True
                    self._downloadingTime = round(duration, 3)
                    filename = self.extractNameFromHeader(response)
                    self._filePath = filename
                    self._fileSize = len(response.content)
                    saved = saveAsFile(response, outPath, filename, overwrite)
                    if   saved == 0:
                        pass
                    elif saved == -2:
                        if self._retries > 1:
                            print('') # new line if required
                        print('   Skipping "{:s}": File already exists.'.format(self._filePath))
                        self._status = 777
                    else:
                        raise Exception('An error ocurred when saving the file "{:}"'.format(filename))
                
                elif self._status == 202:
                    # Still processing, wait and retry
                    log.logMessage(response.json())
                    sleep(pollPeriod)
                
                elif self._status == 204:
                    # No data found
                    print('   No data found.')

                elif self._status == 400:
                    # API Error
                    _printErrorMessage(response)
                    raise Exception('The request failed with HTTP status {:d}.'.format(self._status), response.json())
                
                elif self._status == 404:
                    # Index too high, no more files to download
                    log.printNewLine()
                    pass

                else:
                    # Gone
                    print('   FTP Error: File not found. If this product order is recent, retry downloading this product using the method downloadProduct with the runId: ' + runId)
                    _printErrorMessage(response)
            except Exception as ex:
                raise

        return self._status


    def extractNameFromHeader(self, response):
        """
        In a download request response 200, extracts and returns the file name from the response
        """
        txt = response.headers['Content-Disposition']
        filename = txt.split('filename=')[1]
        return filename

    def setComplete(self):
        self._status = 200


    def getInfo(self):
        errorCodes = {
            '200': 'complete',
            '202': 'running',
            '204': 'no content',
            '400': 'error',
            '401': 'unauthorized',
            '404': 'not found',
            '410': 'gone',
            '500': 'server error',
            '777': 'skipped'
        }

        txtStatus = errorCodes[str(self._status)]
        
        return {
            'url'             : self._downloadUrl,
            'status'          : txtStatus,
            'size'            : self._fileSize,
            'file'            : self._filePath,
            'index'           : self._filters['index'],
            'downloaded'      : self._downloaded,
            'requestCount'    : self._retries,
            'fileDownloadTime': float(self._downloadingTime)
        }