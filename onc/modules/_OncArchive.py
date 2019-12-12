from ._OncService import _OncService
from ._MultiPage import _MultiPage
import requests
import json
import humanize
import os
import time

from ._util import saveAsFile, _printErrorMessage, _formatDuration

class _OncArchive(_OncService):
    """
    Methods that wrap the API archivefiles service
    """

    def __init__(self, parent: object):
        super().__init__(parent)


    def getListByLocation(self, filters: dict=None, allPages: bool=False):
        """
        Get a list of files for a given location code and device category code, and filtered by others optional parameters.
        if locationCode or deviceCategoryCode are missing, we suppose they are in the filters
        """
        try:
            return self._getList(filters, by='location', allPages=allPages)
        except Exception: raise


    def getListByDevice(self, filters: dict=None, allPages: bool=False):
        """
        Get a list of files available in Oceans 2.0 Archiving System for a given device code. The list of filenames can be filtered by time range.
        if deviceCode is missing, we suppose it is in the filters
        """
        try:
            return self._getList(filters, by='device', allPages=allPages)
        except Exception: raise


    def getFile(self, filename: str='', overwrite: bool=False):
        url = self._serviceUrl('archivefiles')
        
        filters = {
            'token'   : self._config('token'),
            'method'  : 'getFile',
            'filename': filename
        }

        try:
            # Download the archived file with filename (response contents is binary)
            start = time.time()
            response = requests.get(url, filters, timeout=self._config('timeout'))
            status = response.status_code
            elapsed = time.time() - start
            
            if response.ok:
                # Save file to output path
                outPath = self._config('outPath')
                saveAsFile(response, outPath, filename, overwrite)
                filePath = '{:s}/{:s}'.format(outPath, filename)
                #self._fixGzFileExtension(filePath) # Supposedly not needed after DMAS fix
                
            else:
                _printErrorMessage(response)
                if status == 400:
                    raise Exception('   The request failed with HTTP status 400.', response.json())
                else:
                    raise Exception('   The request failed with HTTP status {:d}.'.format(status), response.text)

        except Exception: raise

        # Prepare a readable status
        txtStatus = "error"
        if status == 200:
            txtStatus = "completed"
        
        return {
            'url'         : response.url,
            'status'      : txtStatus,
            'size'        : len(response.content),
            'downloadTime': round(elapsed, 3),
            'file'        : filename
        }


    def getDirectFiles(self, filters: dict, overwrite: bool=False, allPages: bool=False):
        '''
        Method to download files from the archivefiles service 
        see https://wiki.oceannetworks.ca/display/help/archivefiles for usage and available filters
        '''
        # make sure we only get a simple list of files
        if 'returnOptions' in filters:
            del filters['returnOptions']

        # Get a list of files
        try:
            if 'locationCode' in filters and 'deviceCategoryCode' in filters:
                dataRows = self.getListByLocation(filters=filters, allPages=allPages)
            elif 'deviceCode' in filters:
                dataRows = self.getListByDevice(filters=filters, allPages=allPages)
            else:
                raise Exception('getDirectFiles filters require either a combination of "locationCode" and "deviceCategoryCode", or a "deviceCode" present.')
        except Exception: raise
        
        n = len(dataRows['files'])
        print('Obtained a list of {:d} files to download.'.format(n))

        # Download the files obtained
        tries = 1
        successes = 0
        size = 0
        time = 0
        downInfos = []
        for filename in dataRows['files']:
            # only download if file doesn't exist (or overwrite is True)
            outPath = self._config('outPath')
            filePath = '{:s}/{:s}'.format(outPath, filename)
            fileExists = os.path.exists(filePath)
            
            if (not fileExists) or (fileExists and overwrite):
                print('   ({:d} of {:d}) Downloading file: "{:s}"'.format(tries, n, filename))
                try:
                    downInfo = self.getFile(filename, overwrite)
                    size += downInfo['size']
                    time += downInfo['downloadTime']
                    downInfos.append(downInfo)
                    successes += 1
                except Exception: raise
                tries += 1
            else:
                print('   Skipping "{:s}": File already exists.'.format(filename))
                downInfo = {
                    'url'         : self._getDownloadUrl(filename),
                    'status'      : 'skipped',
                    'size'        : 0,
                    'downloadTime': 0,
                    'file'        : filename
                }
                downInfos.append(downInfo)

        print('{:d} files ({:s}) downloaded'.format(successes, humanize.naturalsize(size)))
        print('Total Download Time: {:s}'.format(_formatDuration(time)))

        return {
            'downloadResults': downInfos,
            'stats': {
                'totalSize'   : size,
                'downloadTime': time,
                'fileCount'   : successes
            }
        }

    def _getDownloadUrl(self, filename: str):
        """
        Returns an archivefile absolute download URL for a filename
        """
        url = self._serviceUrl('archivefiles')
        return '{:s}?method=getFile&filename={:s}&token={:s}'.format(url, filename, self._config('token'))


    def _getList(self, filters: dict, by: str='location', allPages: bool=False):
        """
        Wraps archivefiles getListByLocation and getListByDevice methods
        """
        url = self._serviceUrl('archivefiles')
        filters['token'] = self._config('token')
        filters['method'] = 'getListByLocation' if by == 'location' else 'getListByDevice'

        # parse and remove the artificial parameter extension
        extension = None
        filters2 = filters.copy()
        if 'extension' in filters2:
            extension = filters2['extension']

        try:
            if allPages:
                mp = _MultiPage(self)
                result = mp.getAllPages('archivefiles', url, filters2)
            else:
                if 'extension' in filters2:
                    del filters2['extension']
                result = self._doRequest(url, filters2)
                result = self._filterByExtension(result, extension)
            return result
        except Exception: raise


    def _filterByExtension(self, results: dict, extension: str):
        '''
        Filter results to only those where filenames end with the extension
        If extension is None, won't do anything
        Returns the filtered list
        '''
        if extension is None:
            return results

        extension = '.' + extension # match the dot to avoid matching substrings
        n = len(extension)
        filtered = [] # appending is faster than deleting
        
        # determine the row structure
        rowFormat = 'filename'
        if len(results['files']) > 0:
            if isinstance(results['files'][0], dict):
                rowFormat = 'dict'

        # filter
        for file in results['files']:
            if rowFormat == 'filename':
                if file[-n:] == extension:
                    filtered.append(file)   
            else:
                if file['filename'][-n:] == extension:
                    filtered.append(file)
        results['files'] = filtered

        return results