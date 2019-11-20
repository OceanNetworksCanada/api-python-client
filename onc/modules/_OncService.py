import requests
from urllib import parse
import weakref
from time import time
from ._util import _printErrorMessage, _messageForError, _formatDuration

class _OncService:
    """
    Provides common configuration and functionality to Onc service classes (children)
    """

    def __init__(self, parent: object):
        self.parent = weakref.ref(parent)
        

    def _doRequest(self, url: str, filters: dict=None, getTime=False):
        """
        Generic request wrapper for making simple web service requests
        @param url:    String full url to request
        @param params: Dictionary of parameters to append to the request
        @return:       if getTime is True: A tuple (jsonResponse, responseTime), otherwise just jsonResult
        @throws:       Exception if the HTTP request fails with status 400, as a tuple with
                       the error description and the error JSON structure returned
                       by the API, or a generic exception otherwise
        """
        if filters is None: filters = {}
        timeout = self._config('timeout')
        
        try:
            txtParams = parse.unquote(parse.urlencode(filters))
            self._log('Requesting URL:\n{:s}?{:s}'.format(url, txtParams))
            
            start = time()
            response = requests.get(url, filters, timeout=timeout)
            responseTime = time() - start
            
            if response.ok:
                jsonResult = response.json()
            else:
                status = response.status_code
                if status == 400:
                    _printErrorMessage(response)
                    raise Exception('The request failed with HTTP status {:d}.'.format(status), response.json())
                elif status == 401:
                    print('ERROR: Invalid user token.')
                    raise Exception('Invalid user token (status 401).', response.json())
                elif status == 503:
                    print('ERROR 503: Service unavailable. We could be down for maintenance; visit data.oceannetworks.ca for more information.')
                    raise Exception('Service unavailable (status 503)')
                else:
                    raise Exception('The request failed with HTTP status {:d}.'.format(status), _messageForError(status))

            self._log('Web Service response time: {:s}'.format(_formatDuration(responseTime)))
        
        except requests.exceptions.Timeout:
            raise Exception('The request ran out of time (timeout: {:d} s)'.format(timeout)) from None
        except Exception:
            raise

        if getTime:
            return jsonResult, responseTime
        else:
            return jsonResult


    def _serviceUrl(self, service: str):
        """
        Returns the absolute url for a given ONC API service
        """
        if service in ['locations', 'deployments', 'devices', 'deviceCategories', 'properties', 'dataProducts', 'archivefiles', 'scalardata', 'rawdata']:
            return '{:s}api/{:s}'.format(self._config('baseUrl'), service)
        
        return ''


    def _log(self, message: str):
        """
        Prints message to console only when self.showInfo is true
        @param message: String
        """
        if self._config('showInfo'):
            print(message)


    def _config(self, key: str):
        """
        Returns a property from the parent (ONC class)
        """
        return getattr(self.parent(), key)