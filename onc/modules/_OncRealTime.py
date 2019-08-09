from ._OncService import _OncService
from ._MultiPage import _MultiPage

class _OncRealTime(_OncService):
    """
    Near real-time services methods
    """

    def __init__(self, config: dict):
        super().__init__(config)


    def getDirectByLocation(self, filters: dict, allPages: bool):
        '''
        Method to return scalar data from the scalardata service in JSON Object format
        see https://wiki.oceannetworks.ca/display/help/scalardata+service for usage and available filters
        '''
        return self._getDirectAllPages(filters, 'scalardata', 'getByLocation', allPages)


    def getDirectByDevice(self, filters: dict, allPages: bool):
        '''
        Method to return scalar data from the scalardata service
        see https://wiki.oceannetworks.ca/display/help/scalardata+service for usage and available filters
        '''
        return self._getDirectAllPages(filters, 'scalardata', 'getByDevice', allPages)


    def getDirectRawByLocation(self, filters: dict, allPages: bool):
        '''
        Method to return raw data from an instrument, in the payload, in JSON format from the rawdata service 
        see https://wiki.oceannetworks.ca/display/help/rawdata+service for usage and available filters
        '''
        return self._getDirectAllPages(filters, 'rawdata', 'getByLocation', allPages)


    def getDirectRawByDevice(self, filters: dict, allPages: bool):
        '''
        Method to return raw data from an instrument, in the payload, in JSON format from the rawdata service 
        see https://wiki.oceannetworks.ca/display/help/rawdata+service for usage and available filters
        '''
        return self._getDirectAllPages(filters, 'rawdata', 'getByDevice', allPages)


    def _getDirectAllPages(self, filters: dict, service: str, method: str, allPages: bool):
        '''
        Keeps downloading all scalar or raw data pages until finished
        Automatically translates sensorCategoryCodes to a string if a list is provided
        Return the full stitched data
        '''
        # prepare filters for first page request
        filters = filters or {}
        url = self._serviceUrl(service)
        filters['method'] = method
        filters['token'] = self._config('token')
        dataKey = 'sensorData' if service == 'scalardata' else 'data'

        # if sensorCategoryCodes is an array, join it into a comma-separated string
        if 'sensorCategoryCodes' in filters and isinstance(filters['sensorCategoryCodes'], list):
            filters['sensorCategoryCodes'] = ",".join(filters['sensorCategoryCodes'])

        try:
            if allPages:
                mp = _MultiPage(self)
                result = mp.getAllPages(service, url, filters)
            else:
                result = self._doRequest(url, filters)
            return result
        except Exception: raise