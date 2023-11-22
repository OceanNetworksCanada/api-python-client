import weakref
from time import time
from urllib import parse

import requests

from ._util import _formatDuration, _messageForError, _printErrorMessage


class _OncService:
    """
    Provides common configuration and functionality to Onc service classes (children)
    """

    def __init__(self, parent: object):
        self.parent = weakref.ref(parent)

    def _doRequest(self, url: str, filters: dict = None, getTime=False):
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


        Raises
        ------
        Exception
            If the HTTP request fails with status 400, as a tuple with
            the error description and the error JSON structure returned
            by the API, or a generic exception otherwise.
        """
        if filters is None:
            filters = {}
        timeout = self._config("timeout")

        try:
            txtParams = parse.unquote(parse.urlencode(filters))
            self._log(f"Requesting URL:\n{url}?{txtParams}")

            start = time()
            response = requests.get(url, filters, timeout=timeout)
            responseTime = time() - start

            if response.ok:
                jsonResult = response.json()
            else:
                status = response.status_code
                if status == 400:
                    _printErrorMessage(response)
                    raise Exception(
                        f"The request failed with HTTP status {status}.",
                        response.json(),
                    )
                elif status == 401:
                    print("ERROR: Invalid user token.")
                    raise Exception("Invalid user token (status 401).", response.json())
                elif status == 503:
                    print(
                        "ERROR 503: Service unavailable. We could be down for maintenance;"  # noqa: E501
                        "visit https://data.oceannetworks.ca for more information."
                    )
                    raise Exception("Service unavailable (status 503)")
                else:
                    raise Exception(
                        f"The request failed with HTTP status {status}.",
                        _messageForError(status),
                    )

            self._log(f"Web Service response time: {_formatDuration(responseTime)}")

        except requests.exceptions.Timeout:
            raise Exception(
                f"The request ran out of time (timeout: {timeout} s)"
            ) from None
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
