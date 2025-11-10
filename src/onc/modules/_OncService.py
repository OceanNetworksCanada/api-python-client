from __future__ import annotations

import logging
import pprint
import weakref
from time import time
from urllib import parse

import requests

from ._util import _createErrorMessage, _formatDuration
from onc.modules._Messages import (setup_logger,
                                   build_error_message,
                                   scrub_token,
                                   REQ_MSG,
                                   RESPONSE_TIME_MSG,
                                   RESPONSE_MSG)

logging.basicConfig(format="%(levelname)s: %(message)s")


class _OncService:
    """
    Provides common configuration and functionality to Onc service classes (children)
    """

    def __init__(self, parent: object,
                 verbosity: str,
                 redact_token: bool,
                 raise_http_errors: bool):
        self.parent = weakref.ref(parent)
        self.redact_token = redact_token
        self.raise_http_errors = raise_http_errors
        self.verbosity = verbosity

        self.__log = setup_logger('onc-service', level = verbosity)

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

        response = requests.get(url, filters, timeout=timeout)

        if self.redact_token is True:
            try:
                response_url = scrub_token(response.url)
            except:
                response_url = response.url
        else:
            response_url = response.url

        # Log the url the user submitted.
        self.__log.info(REQ_MSG.format(response_url))

        # Display the time it took for ONC to respond in seconds.
        # The requests.Response.elapsed value is a datetime.timedelta object.
        responseTime = round(response.elapsed.total_seconds(),3) # To milliseconds.
        self.__log.debug(RESPONSE_TIME_MSG.format(responseTime))

        json_response = response.json()

        if response.status_code == requests.codes.ok:
            self.__log.info(RESPONSE_MSG.format("OK", response.status_code))
            if getTime is True:
                return json_response, responseTime
            else:
                return json_response
        else:
            if response.status_code == requests.codes.not_found:
                self.__log.error(RESPONSE_MSG.format("Not Found",
                                                     response.status_code))
            elif response.status_code == requests.codes.bad:
                self.__log.error(RESPONSE_MSG.format("Bad Request",
                                                     response.status_code))
            elif response.status_code == requests.codes.unauthorized:
                self.__log.error(RESPONSE_MSG.format("Unauthorized Request",
                                                     response.status_code))
            elif response.status_code == requests.codes.internal_server_error:
                self.__log.error(RESPONSE_MSG.format("Internal Server Error",
                                                     response.status_code))
            else:
                self.__log.error(RESPONSE_MSG.format('Error',response.status_code))

            self.__log.error(build_error_message(response,
                                                 self.redact_token))

            if self.raise_http_errors is True:
                response.raise_for_status()

            else:
                if getTime is True:
                    return response, responseTime
                else:
                    return response


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
        ]:
            return f"{self._config('baseUrl')}api/{service}"

        return ""

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

