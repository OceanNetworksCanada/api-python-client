from typing import Any

from ._MultiPage import _MultiPage
from ._OncService import _OncService


class _OncRealTime(_OncService):
    """
    Near real-time services methods
    """

    def __init__(self, config: dict):
        super().__init__(config)

    def getDirectByLocation(self, filters: dict, allPages: bool):
        """
        Return scalar data readings from a device category in a location.

        See https://wiki.oceannetworks.ca/display/O2A/scalardata+service
        for usage and available filters
        """
        return self._getDirectAllPages(filters, "scalardata", "getByLocation", allPages)

    def getDirectByDevice(self, filters: dict, allPages: bool):
        """
        Return scalar data readings from a device.

        See https://wiki.oceannetworks.ca/display/O2A/scalardata+service
        for usage and available filters.
        """
        return self._getDirectAllPages(filters, "scalardata", "getByDevice", allPages)

    def getDirectRawByLocation(self, filters: dict, allPages: bool):
        """
        Return raw data readings from a device category in a location.

        See https://wiki.oceannetworks.ca/display/O2A/rawdata+service
        for usage and available filters.
        """
        return self._getDirectAllPages(filters, "rawdata", "getByLocation", allPages)

    def getDirectRawByDevice(self, filters: dict, allPages: bool):
        """
        Return raw data readings from an device.

        See https://wiki.oceannetworks.ca/display/O2A/rawdata+service
        for usage and available filters.
        """
        return self._getDirectAllPages(filters, "rawdata", "getByDevice", allPages)

    def getSensorCategoryCodes(self, filters: dict):
        updated_filters = filters | {"returnOptions": "excludeScalarData"}
        if "deviceCode" in filters:
            return self.getDirectByDevice(updated_filters, False)["sensorData"]
        else:
            return self.getDirectByLocation(updated_filters, False)["sensorData"]

    def _getDirectAllPages(
        self, filters: dict, service: str, method: str, allPages: bool
    ) -> Any:
        """
        Keeps downloading all scalar or raw data pages until finished.

        Automatically translates sensorCategoryCodes to a string if a list is provided.

        Returns
        -------
            The full stitched data.
        """
        # prepare filters for first page request
        filters = filters or {}
        url = self._serviceUrl(service)
        filters["method"] = method
        filters["token"] = self._config("token")

        # if sensorCategoryCodes is an array, join it into a comma-separated string
        if "sensorCategoryCodes" in filters and isinstance(
            filters["sensorCategoryCodes"], list
        ):
            filters["sensorCategoryCodes"] = ",".join(filters["sensorCategoryCodes"])

        if allPages:
            mp = _MultiPage(self)
            result = mp.getAllPages(service, url, filters)
        else:
            result = self._doRequest(url, filters)
        return result
