import os
import json
from expectedfields import expectedFields
from env_variable import token

from onc.onc import ONC
onc = ONC(token, True, True, 'output')

def runMethod(name: str, filters: dict, param1=None):
    """
    Runs a method from the global onc object
    optionally allows for a second nameless parameter
    """
    if   name == 'getLocations'           : return onc.getLocations(filters)
    elif name == 'getLocationHierarchy'   : return onc.getLocationHierarchy(filters)
    elif name == 'getDeployments'         : return onc.getDeployments(filters)
    elif name == 'getDevices'             : return onc.getDevices(filters)
    elif name == 'getDeviceCategories'    : return onc.getDeviceCategories(filters)
    elif name == 'getProperties'          : return onc.getProperties(filters)
    elif name == 'getDataProducts'        : return onc.getDataProducts(filters)
    elif name == 'getDirectScalar'        : return onc.getDirectScalar(filters, param1)
    elif name == 'getDirectByLocation'    : return onc.getDirectByLocation(filters, param1)
    elif name == 'getDirectByDevice'      : return onc.getDirectByDevice(filters, param1)
    elif name == 'getDirectRawByLocation' : return onc.getDirectRawByLocation(filters, param1)
    elif name == 'getDirectRawByDevice'   : return onc.getDirectRawByDevice(filters, param1)
    elif name == 'getListByLocation'      : return onc.getListByLocation(filters, param1)
    elif name == 'getListByDevice'        : return onc.getListByDevice(filters, param1)


def makeOnc(token: str, outPath='output'):
    # Returns a onc instance
    return ONC(token, True, True, outPath)


def dataHasExpectedFields(data, methodName):
    # True if data is an element with the fields and types described in
    #   the expectedFields global
    #   False otherwise, and prints an error message as hint
    expected = expectedFields[methodName]
    for expectedField, expectedType in expected.items():
        # can this field be null?
        canBeNull = False
        if expectedType[-1] == '*':
            expectedType = expectedType[:-1]
            canBeNull = True

        # Is the field present?
        if expectedField in data:
            value = data[expectedField]
            ty = type(value).__name__
            print('Type of field "{:s}" is "{:s}"'.format(expectedField, ty))

            # Is the type as expected?
            if not(canBeNull and (ty == "NoneType")):
                if ty != expectedType:
                    print('Type of field "{:s}" is "{:s}" but was expected "{:s}"'.format(expectedField, ty, expectedType))
                    return False
        else:
            print('Field "{:s}" not found'.format(expectedField))
            return False
    return True


def isOncInstalled():
    '''
    Returns True if the onc package is installed
    '''
    try:
        from onc.onc import ONC
    except ImportError:
        return False
    return True


def saveJsonToFile(obj: dict, filepath: str):
    '''
    saves a json dictionary structure to a file
    tries to beautify the output
    '''
    # create path if it doesn't exist
    path, filename = os.path.split(filepath)
    if not os.path.exists(path):
        os.makedirs(path)

    text = json.dumps(obj, indent=4)
    with open(filepath, 'w+') as file:
        file.write(text)

