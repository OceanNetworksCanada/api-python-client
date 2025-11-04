from __future__ import annotations

import logging
import pprint
import weakref
from time import time
from urllib import parse

import requests

from ._util import _createErrorMessage, _formatDuration

logging.basicConfig(format="%(levelname)s: %(message)s")


class _OncService:
    """
    Provides common configuration and functionality to Onc service classes (children)
    """

    def __init__(self, parent: object):
        self.parent = weakref.ref(parent)

    def _doRequest(self, url: str, filters: dict | None = None, getTime: bool = False):
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
        filters["token"] = self._config("token")
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
            if status in [400, 401]:
                msg = _createErrorMessage(response)
                raise requests.HTTPError(msg)
            else:
                response.raise_for_status()
        self._log(f"Web Service response time: {_formatDuration(responseTime)}")

        # Log warning messages only when showWarning is True
        # and jsonResult["messages"] is not an empty list
        if (
            self._config("showWarning")
            and "messages" in jsonResult
            and jsonResult["messages"]
        ):
            long_message = "\n".join(
                [f"* {message}" for message in jsonResult["messages"]]
            )

            filters_without_token = filters.copy()
            del filters_without_token["token"]
            filters_str = pprint.pformat(filters_without_token)

            logging.warning(
                f"When calling {url} with filters\n{filters_str},\n"
                f"there are several warning messages:\n{long_message}\n"
            )

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
            "archivefile",
            "scalardata",
            "rawdata",
            "dataAvailability/dataproducts",
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

    def _delegateByFilters(self, byDevice, byLocation, **kwargs):
        """
        Delegate getX helper methods into getXByDevice or getXByLocation methods.
        """
        filters = kwargs["filters"]

        if "deviceCode" in filters:
            return byDevice(**kwargs)
        elif "locationCode" in filters and "deviceCategoryCode" in filters:
            return byLocation(**kwargs)
        else:
            raise ValueError(
                "Query parameters require either a combination of "
                "'locationCode' and 'deviceCategoryCode', "
                "or a 'deviceCode' present."
            )
