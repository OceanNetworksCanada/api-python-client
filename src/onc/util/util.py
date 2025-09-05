# ------------------------------------------------------------------------------
# Name:        util
# Purpose:     This is a collection of utility functions used the ONC library
#
# Author:      ryanross
#
# Created:     31/10/2016
# Copyright:   (c) Ocean Networks Canada 2016-2018
# Licence:     None
# Requires:    requests library - [Python Install]\scripts\pip install requests
# ------------------------------------------------------------------------------

import json
import math
from dateutil.relativedelta import SU, relativedelta
import os
from datetime import datetime, timedelta
from netrc import netrc
import pandas as pd

datetimeFormat = "%Y-%m-%dT%H:%M:%S.%f"
FlagTerm = 'flag'  # String that prepends in pandas/xarray to indicate a flag variable.


def printErrorMessage(response, parameters, showUrl=False, showValue=False):
    """
    Print an error message from an ONC web service call to the console.
    """
    if response.status_code == 400:
        if showUrl:
            print(f"Error Executing: {response.url}")
        payload = json.loads(str(response.content, "utf-8"))
        if len(payload) >= 1:
            for e in payload["errors"]:
                code = e["errorCode"]
                msg = e["errorMessage"]
                parm = e["parameter"]

                matching = [p for p in parm.split(",") if p in parameters]
                if len(matching) >= 1:
                    for p in matching:
                        print(
                            f"  Error {code}: {msg}. Parameter '{p}' with value '{parameters[p]}'"  # noqa: E501
                        )
                else:
                    print(f"  '{msg}' for {parm}")

                if showValue:
                    for p in parm.split(","):
                        parmValue = parameters[p]
                        print(f"  {msg} for {p} - value: '{parmValue}'")

            return payload

    else:
        msg = f"Error {response.status_code} - {response.reason}"
        print(msg)
        return msg


def printCount(count, name):
    """
    Print a count with a name to the console.
    """
    if count != 1:
        print(f"  {count} {name}")


def printResponseTime(end, start):
    """
    Print a time duration of a web service call to the console.
    """
    delta = end - start
    execTime = round(delta.seconds + delta.microseconds / 1e6, 3)
    print(f"Web Service response time: {execTime} seconds")


def getHMS(seconds):
    """
    Convert a time value in seconds to a string in the format Hours:Minutes:Seconds.
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:.0f}:{m:.0f}:{s:.2f}"


def printHMS(seconds):
    """
    Print a time value in seconds as string in the format Hours:Minutes:Seconds
    to the console.
    """
    print(getHMS(seconds))


def convertSize(size):
    """
    Return a string representation of a size in bytes.
    """
    if size == 0:
        return "0 KB"
    sizeUnits = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return f"{s} {sizeUnits[i]}"


def toBytes(str):
    """
    Return a size in bytes from a string representation of a file size
    """
    iBytes = None
    if str:
        sizeUnits = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        sSize = str.split(" ")[0]
        if isNumber(sSize):
            nSize = float(sSize)
        else:
            return None

        sName = str.split(" ")[1]
        if sName in sizeUnits:
            indx = sizeUnits.index(sName)
            p = math.pow(1024, indx)
            iBytes = int(p * nSize)
        else:
            print(f"Unable to convert to bytes - '{sName}' is an unknown size unit.")

    return iBytes


def toSeconds(str):
    """
    Return a time in seconds from a string representing a time
    """
    seconds = None
    if str:
        timeUnits = ("s", "min", "h")
        sSize = str.split(" ")[0]
        if isNumber(sSize):
            iSize = float(sSize)
        else:
            return None

        sName = str.split(" ")[1]
        if sName in timeUnits:
            indx = timeUnits.index(sName)
            p = math.pow(60, indx)
            seconds = int(p * iSize)
        else:
            print(f"Unable to convert to seconds - '{sName}' is an unknown time unit.")

    return seconds


def printWithEnd(message, separator=None):
    """
    Print a message to the console without a line break.

    This allows for writing subsequent messages to the same line,
    such as Downloading.....
    """
    if separator:
        print(message, end="", sep=separator)
    else:
        print(message, end="")


def readJSONFile(filename):
    """
    Read JSON from a file and return it as an object.
    """
    j = None
    with open(filename) as f:
        j = json.loads(f.read())

    return j


def writeJSONFile(filename, obj, sort=False):
    """
    Write an object as JSON to a file.
    """
    s = json.dumps(obj, sort_keys=sort, indent=4, separators=(",", ": "))
    with open(filename, "w") as f:
        f.write(s)


def toString(obj):
    """
    Return the string representation of an object.
    """
    return str(obj, "utf-8")


def isNumber(obj):
    """
    Check if an object is a valid number.
    """
    try:
        float(obj)
        return True
    except ValueError:
        return False


def daterangeByDay(startDate, endDate):
    """
    Split a date range into a list of day date range objects.
    """
    dtStart = datetime(startDate.year, startDate.month, startDate.day)
    dtEnd = dtStart + timedelta(days=1)
    if dtEnd > endDate:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
        }
    else:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
        }

        while True:
            dtStart = dtEnd
            dtEnd = dtStart + relativedelta(days=1)
            if dtEnd > endDate:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
                }
                break
            else:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
                }


def daterangeByWeek(startDate, endDate, dayOfWeek=SU):  # MO TU, WE, TH, FR, SA, SU
    """
    Split a date range into a list of week date range objects.

    The method accepts a parameter to specifiy the beginning of the week.
    """
    newStart = startDate + relativedelta(weekday=dayOfWeek(-1))

    dtStart = datetime(newStart.year, newStart.month, newStart.day)
    dtEnd = dtStart + relativedelta(weeks=1)
    if dtEnd > endDate:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
        }
    else:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
        }

        while True:
            dtStart = dtEnd
            dtEnd = dtStart + relativedelta(weeks=1)
            if dtEnd > endDate:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
                }
                break
            else:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
                }


def daterangeByMonth(startDate, endDate):
    """
    Split a date range into a list of month date range objects by month.
    """
    dtStart = datetime(startDate.year, startDate.month, 1)
    dtEnd = dtStart + relativedelta(months=1)
    if dtEnd > endDate:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
        }
    else:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
        }

        while True:
            dtStart = dtEnd
            dtEnd = dtStart + relativedelta(months=1)
            if dtEnd > endDate:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
                }
                break
            else:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
                }


def daterangeByYear(startDate, endDate):
    """
    Split a date range into a list of year date range objects.
    """
    dtStart = datetime(startDate.year, 1, 1)
    dtEnd = dtStart + relativedelta(years=1)
    if dtEnd > endDate:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
        }
    else:
        yield {
            "begin": startDate.strftime(datetimeFormat)[:-3] + "Z",
            "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
        }

        while True:
            dtStart = dtEnd
            dtEnd = dtStart + relativedelta(years=1)
            if dtEnd > endDate:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": endDate.strftime(datetimeFormat)[:-3] + "Z",
                }
                break
            else:
                yield {
                    "begin": dtStart.strftime(datetimeFormat)[:-3] + "Z",
                    "end": dtEnd.strftime(datetimeFormat)[:-3] + "Z",
                }


def copyFieldIfExists(fromDic, toDic, keys):
    """
    Copy the field at name from fromDic to toDic only if it exists

    @param fromDic: Origin Dictionary
    @param toDic: Destination Dictionary
    @param keys: Array of keys of the elements to copy
    """
    for key in keys:
        if key in fromDic:
            toDic[key] = fromDic[key]


def dt2str(dt: datetime) -> str:
    """
    Convert a Pythonic datetime object to a string that is compatible
    with the ONC Oceans 3.0 API dateFrom and dateTo API query parameters.


    Parameters
    ----------
    dt: datetime
        A Python datetime object.

    Returns
    -------
    str

    Examples
    ----------
    >>> dtstr = dt2str(datetime.now()) # doctest: +SKIP
    """

    dt = pd.to_datetime(dt)
    dtstr = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return dtstr


def get_onc_token(netrc_path: os.PathLike | None = None) -> str:
    """
    Retrieve an ONC token from the password portion of a .netrc file entry.

    machine data.oceannetworks.ca
    login <username>
    password <onc_token>

    Parameters
    ----------
    netrc_path: os.PathLike | None
        The path to the .netrc file.
        If left as the default value of None, the netrc module looks for a
        .netrc file in the user directory. If None, the netrc module looks for a
        .netrc file in the user directory.


    Returns
    -------
    str

    Examples
    ----------
    >>> token = get_onc_token() # doctest: +SKIP
    """

    if netrc_path is None:
        _, __, onc_token = netrc().authenticators("data.oceannetworks.ca")
    else:
        _, __, onc_token = netrc(netrc_path).authenticators("data.oceannetworks.ca")
    return onc_token
