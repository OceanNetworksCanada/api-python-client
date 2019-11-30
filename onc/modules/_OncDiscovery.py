from ._OncService import _OncService

class _OncDiscovery(_OncService):
    """
    Methods that wrap the API discovery services:
        locations, deployments, devices, deviceCategories, properties, dataProducts
    """
    
    def __init__(self, parent: object):
        super().__init__(parent)


    def _discoveryRequest(self, filters: dict, service: str, method: str='get'):
        url = self._serviceUrl(service)
        filters['method'] = method
        filters['token'] = self._config('token')

        try:
            result = self._doRequest(url, filters)
            self._sanitizeBooleans(result)
            return result
        except Exception: raise


    def getLocations(self, filters: dict):
        """Requests and returns a filtered list of locations. Wraps the "locations" API web service.
        @param filters: Filters in the API request
        @return: list of dictionaries returned by the API
        """
        filters = filters or {}
        return self._discoveryRequest(filters, service='locations')


    def getLocationHierarchy(self, filters: dict):
        filters = filters or {}
        return self._discoveryRequest(filters, service='locations', method='getTree')


    def getDeployments(self, filters: dict):
        filters = filters or {}
        return self._discoveryRequest(filters, service='deployments')


    def getDevices(self, filters: dict):
        filters = filters or {}
        return self._discoveryRequest(filters, service='devices')


    def getDeviceCategories(self, filters: dict):
        filters = filters or {}
        return self._discoveryRequest(filters, service='deviceCategories')


    def getProperties(self, filters: dict):
        filters = filters or {}
        return self._discoveryRequest(filters, service='properties')


    def getDataProducts(self, filters: dict):
        filters = filters or {}
        return self._discoveryRequest(filters, service='dataProducts')


    def _sanitizeBooleans(self, data: list):
        """
        For all rows in data, enforce that fields expected to have bool values have the right type
            Will modify the data array
        @param data:   Usually an array of dictionaries
        """
        if not(isinstance(data, list)): return
        if len(data) == 0: return

        fixHasDeviceData = False
        fixHasPropertyData = False

        # check hasDeviceData only if present and of the wrong type
        # for now we only check the first row
        if "hasDeviceData" in data[0]:
            if (type(data[0]["hasDeviceData"]) != bool):   fixHasDeviceData = True
        
        if "hasPropertyData" in data[0]:
            if (type(data[0]["hasPropertyData"]) != bool): fixHasPropertyData = True

        # same for hasPropertyData
        if fixHasDeviceData or fixHasPropertyData:
            for row in data:
                if fixHasDeviceData:
                    row["hasDeviceData"]   = (row["hasDeviceData"] == "true")
                if fixHasPropertyData:
                    row["hasPropertyData"] = (row["hasPropertyData"] == "true")
                
                # repeat for "children" if any
                if 'children' in row:
                    self._sanitizeBooleans(row["children"])
