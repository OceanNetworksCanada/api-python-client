from ._OncService import _OncService
from datetime import datetime, timedelta
import requests
import os
import humanize
from time import sleep, time
from ._DataProductFile import _DataProductFile
from ._PollLog import _PollLog
from .Exceptions import MaxRetriesException
from ._util import _printErrorMessage, _formatSize


class _OncDelivery(_OncService):
    """
    Methods that wrap the API data product delivery services
    """

    def __init__(self, parent: object):
        super().__init__(parent)
        
        # Default seconds to wait between consecutive download tries of a file
        # (when no estimate processing time is available)
        self.pollPeriod = 2.0


    def orderDataProduct(self, filters: dict, maxRetries: int, downloadResultsOnly: bool, includeMetadataFile: bool, overwrite: bool):
        fileList = []
        try:
            # Request the product
            requestData = self.requestDataProduct(filters)
            
            if downloadResultsOnly:
                # Only run and return links
                runData = self.runDataProduct(requestData['dpRequestId'], waitComplete=True)
                for runId in runData['runIds']:
                    fileList.extend(self._infoForProductFiles(runId, runData['fileCount'], includeMetadataFile))
            else:
                # Run and download files
                runData = self.runDataProduct(requestData['dpRequestId'], waitComplete=False)
                for runId in runData['runIds']:
                    fileList.extend(self._downloadProductFiles(runId, includeMetadataFile, maxRetries, overwrite))
            
            print('')
            self._printProductOrderStats(fileList, runData)
        except Exception: raise

        return self._formatResult(fileList, runData)


    def requestDataProduct(self, filters: dict):
        """
        Data product request
        """
        filters['method'] = 'request'
        filters['token']  = self._config('token')
        try:
            url = '{:s}api/dataProductDelivery'.format(self._config('baseUrl'))
            response = self._doRequest(url, filters)
        except Exception: raise

        self._estimatePollPeriod(response)
        self._printProductRequest(response)
        return response


    def runDataProduct(self, dpRequestId: int, waitComplete: bool):
        """
        Run a product request and optionally wait until the product generation is complete
        Return a dictionary with information of the run process
        """
        status = ''
        log = _PollLog(True)
        url = '{:s}api/dataProductDelivery'.format(self._config('baseUrl'))
        runResult = {'runIds': [], 'fileCount': 0, 'runTime': 0, 'requestCount': 0}
        
        try:
            start = time()
            while status != 'complete':
                response = requests.get(url, {'method': 'run', 'token': self._config('token'), 'dpRequestId': dpRequestId}, timeout=self._config('timeout'))
                code = response.status_code
                runResult['requestCount'] += 1
                
                if response.ok:
                    data = response.json()
                else:
                    _printErrorMessage(response)
                    raise Exception('The server request failed with HTTP status {:d}.'.format(code), code)
                
                if waitComplete:
                    status = data[0]['status']
                    log.logMessage(data)
                    if code != 200:
                        sleep(self.pollPeriod)
                else:
                    status = 'complete'
            
            #self.print(data)
            #print('got filecount {}'.format(data[0]['fileCount']))
            runResult['fileCount'] = data[0]['fileCount']
            runResult['runTime'] = time() - start
            
            # print a new line after the process finishes
            if waitComplete:
                print('')

        except Exception: raise
        
        # gather a list of runIds
        for run in data:
            runResult['runIds'].append(run['dpRunId'])

        return runResult


    def downloadDataProduct(self, runId: int, maxRetries: int, downloadResultsOnly: bool, includeMetadataFile: bool, overwrite: bool):
        '''
        A public wrapper for downloadProductFiles that lets a user download data products with a runId
        '''
        try:
            if downloadResultsOnly:
                fileData = self._infoForProductFiles(runId, 0, includeMetadataFile)
            else:
                fileData = self._downloadProductFiles(runId, includeMetadataFile, maxRetries, overwrite)
        except Exception: raise

        return fileData


    def _downloadProductFiles(self, runId: int, getMetadata: bool, maxRetries: int, overwrite: bool, fileCount: int=0):
        fileList = []
        index = 1
        baseUrl = self._config('baseUrl')
        token = self._config('token')

        # keep increasing index until fileCount or until we get 404
        doLoop = True
        timeout = self._config('timeout')
        print('\nDownloading data product files with runId {:d}...'.format(runId))
        
        dpf = _DataProductFile(runId, str(index), baseUrl, token)
        
        # loop thorugh file indexes
        while doLoop:
            # stop after too many retries
            try:
                status = dpf.download(timeout, self.pollPeriod, self._config('outPath'), maxRetries, overwrite)
            except Exception: raise

            if status == 200 or status == 777:
                # file was downloaded (200), or downloaded & skipped (777)
                fileList.append(dpf.getInfo())
                index += 1
                dpf = _DataProductFile(runId, str(index), baseUrl, token)
            

            elif status != 202 or (fileCount > 0 and index >= fileCount):
                # no more files to download
                doLoop = False
        
        # get metadata if required
        if getMetadata:
            dpf = _DataProductFile(runId, 'meta', baseUrl, token)
            try:
                status = dpf.download(timeout, self.pollPeriod, self._config('outPath'), maxRetries, overwrite)
                if status == 200 or status == 777:
                    fileList.append(dpf.getInfo())
                    doLoop = False
            except Exception as ex:
                print(ex)
                print("   Metadata file was not downloaded")
                fileList.append(dpf.getInfo())

        return fileList


    def _infoForProductFiles(self, dpRunId: int, fileCount: int, getMetadata: bool):
        """
        Returns a list of information dictionaries for each file available for download
        Returned rows will have the same structure as those returned by _DataProductFile.getInfo()
        """
        print('\nObtaining download information for data product files with runId {:d}...'.format(dpRunId))

        # If we don't know the fileCount, get it from the server (takes longer)
        if fileCount <= 0:
            fileCount = self._countFilesInProduct(dpRunId)

        # Build a file list of data product file information
        fileList = []
        indexes = list(range(1, fileCount + 1))
        if getMetadata:
            indexes.append('meta')
        
        for index in indexes:
            dpf = _DataProductFile(dpRunId=dpRunId, index=str(index), baseUrl=self._config('baseUrl'), token=self._config('token'))
            dpf.setComplete()
            fileList.append(dpf.getInfo())

        return fileList


    def _countFilesInProduct(self, runId: int):
        """
        Given a runId, polls the "download" method to count the number of files available for download
        Uses HTTP HEAD to avoid downloading the files
        """
        url = '{:s}api/dataProductDelivery'.format(self._config('baseUrl'))
        filters = {'method': 'download', 'token': self._config('token'), 'dpRunId': runId, 'index': 1}
        status = 200
        n = 0
        
        try:
            while status == 200 or status == 202:
                response = requests.head(url, params=filters, timeout=self._config('timeout'))
                status = response.status_code

                if status == 202:
                    # If the file is still running, wait
                    sleep(self.pollPeriod)
                elif status == 200:
                    # count successful HEAD request
                    filters['index'] += 1
                    n += 1
        except Exception: raise
        
        print('   {:d} files available for download'.format(n))
        return n


    def _printProductRequest(self, response):
        """
        Prints the information from a response given after a data product request
        The request response format might differ depending on the product source (archive or generated on the fly)
        """
        isGenerated = ('estimatedFileSize' in response)
        print('Request Id: {:d}'.format(response['dpRequestId']))
        
        if isGenerated:
            size = response['estimatedFileSize'] # API returns it as a formatted string
            print('Estimated File Size: {:s}'.format(size))
            if 'estimatedProcessingTime' in response:
                print('Estimated Processing Time: {:s}'.format(response['estimatedProcessingTime']))
        else:
            size = _formatSize(response['fileSize'])
            print('File Size: {:s}'.format(size))
            print('Data product is ready for download.')


    def _estimatePollPeriod(self, response):
        """
        Sets a poll period adequate to the estimated processing time
        Longer processing times require longer poll periods to avoid going over maxRetries
        """
        # Parse estimated processing time (if the API returns it, which is not the case with archived data products)
        if 'estimatedProcessingTime' in response:
            txtEstimated = response['estimatedProcessingTime']
            parts = txtEstimated.split(' ')
            if len(parts) == 2:
                unit = parts[1]
                factor = 1
                if unit   == 'min':
                    factor = 60
                elif unit == 'hour':
                    factor = 3600
                total = factor * int(parts[0])
                self.pollPeriod = max(0.02 * total, 1.0) # poll every 2%
                
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
                downloadTime  += file['fileDownloadTime']

        # Print run time
        runTime = timedelta(seconds=runInfo['runTime'])
        print('Total run time: {:s}'.format(humanize.naturaldelta(runTime)))
        
        if downloadCount > 0:
            # Print download time
            if downloadTime < 1.0:
                txtDownTime = '{:.3f} seconds'.format(downloadTime)
            else:
                txtDownTime = humanize.naturaldelta(downloadTime)
            print('Total download Time: {:s}'.format(txtDownTime))

            # Print size and count of files
            print('{:d} files ({:s}) downloaded'.format(downloadCount, humanize.naturalsize(size)))
        else:
            print('No files downloaded.')


    def _formatResult(self, fileList: list, runInfo: dict):
        size = 0
        downloadTime = 0
        requestCount = runInfo['requestCount']
        
        for file in fileList:
            downloadTime += file['fileDownloadTime']
            size         += file['size']
            requestCount += file['requestCount']

        result = {
            'downloadResults': fileList,
            'stats': {
                'runTime'     : round(runInfo['runTime'], 3),
                'downloadTime': round(downloadTime, 3),
                'requestCount': requestCount,
                'totalSize'   : size
            }
        }

        return result