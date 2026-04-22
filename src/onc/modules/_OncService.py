import weakref

import requests
from onc.modules._Messages import (
    REQ_MSG,
    RESPONSE_MSG,
    RESPONSE_TIME_MSG,
    build_error_message,
    scrub_token,
    setup_logger,
)


class _OncService:
    """
    Provides common configuration and functionality to Onc service classes (children)
    """

    def __init__(self, parent: object):
        self.parent = weakref.ref(parent)
        self._log = setup_logger("onc.service", level=self._config("verbosity"))

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

        if self._config("redact_token"):
            response_url = scrub_token(response.url)
        else:
            response_url = response.url

        # Log the url the user submitted.
        self._log.debug(REQ_MSG.format(response_url))

        # Display the time it took for ONC to respond in seconds.
        # The requests.Response.elapsed value is a datetime.timedelta object.
        responseTime = round(response.elapsed.total_seconds(), 3)  # To milliseconds.
        self._log.debug(RESPONSE_TIME_MSG.format(responseTime))

        json_response = response.json()

        # Log warning messages if json_response["messages"] is not an empty list
        if "messages" in json_response and json_response["messages"]:
            for message in json_response["messages"]:
                self._log.warning(f"* {message}")

        if response.status_code in (requests.codes.ok, requests.codes.accepted):
            self._log.debug(RESPONSE_MSG.format(response.reason, response.status_code))
            if getTime:
                return json_response, responseTime
            return json_response
        else:
            self._log.error(RESPONSE_MSG.format(response.reason, response.status_code))

            self._log.error(build_error_message(response, self._config("redact_token")))

            if self._config("raise_http_errors"):
                response.raise_for_status()

            if getTime:
                return response, responseTime
            return response

    def _serviceUrl(self, service: str):
        """
        Returns the absolute url for a given ONC API service
        """
        if service in [
            "locations",
            "locations/tree",
            "deployments",
            "devices",
            "deviceCategories",
            "properties",
            "dataProducts",
            "dataAvailability/dataproducts",
            "archivefile/device",
            "archivefile/location",
            "archivefile/download",
            "scalardata/location",
            "scalardata/device",
            "rawdata/location",
            "rawdata/device",
            "dataProductDelivery/request",
            "dataProductDelivery/run",
            "dataProductDelivery/download",
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
