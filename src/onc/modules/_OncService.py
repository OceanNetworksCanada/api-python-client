import weakref
from time import time
from urllib import parse

import requests

from ._util import _formatDuration, _messageForError, _createErrorMessage


class _OncService:
    """
    Provides common configuration and functionality to Onc service classes (children)
    """

    def __init__(self, parent: object):
        self.parent = weakref.ref(parent)

    def _doRequest(self, url: str, filters: dict | None = None, getTime: bool=False):
        """
        Generic request wrapper for making simple web service requests.

        Parameters
        ----------
        url : str
            String full url to request.
        filters : dict of {str: str} or None, optional
            Dictionary of parameters to append to the request.
        getTime : bool, default False
            If True, also return response time as a tuple.

        Returns
        -------
        jsonResult : Any
            The json-encoded content of a response.
        responseTime : str, optional
            Running time of the response. Only available when getTime is True.
        """
        if filters is None:
            filters = {}
        timeout = self._config("timeout")

        txtParams = parse.unquote(parse.urlencode(filters))
        self._log(f"Requesting URL:\n{url}?{txtParams}")

        start = time()
        response = requests.get(url, filters, timeout=timeout)
        responseTime = time() - start

        if response.ok:
            jsonResult = response.json()
        else:
            status = response.status_code
            msg = _createErrorMessage(response)
            if status == 400:
                raise requests.HTTPError(msg)
            elif status == 401:
                raise requests.HTTPError(msg)
            else:
                response.raise_for_status()
        self._log(f"Web Service response time: {_formatDuration(responseTime)}")

        if getTime:
            return jsonResult, responseTime
        else:
            return jsonResult

    def _serviceUrl(self, service: str):
        """
        Returns the absolute url for a given ONC API service
        """
        if service in [
            "locations",
            "deployments",
            "devices",
            "deviceCategories",
            "properties",
            "dataProducts",
            "archivefiles",
            "scalardata",
            "rawdata",
        ]:
            return f"{self._config('baseUrl')}api/{service}"

        return ""

    def _log(self, message: str):
        """
        Prints message to console only when self.showInfo is true
        @param message: String
        """
        if self._config("showInfo"):
            print(message)

    def _config(self, key: str):
        """
        Returns a property from the parent (ONC class)
        """
        return getattr(self.parent(), key)
