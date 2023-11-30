import os
from datetime import timedelta

import humanize


def saveAsFile(response, filePath: str, fileName: str, overwrite: bool):
    """
    Saves the file downloaded in the response object, in the outPath, with filename
    If overwrite, will overwrite files with the same name
    @returns status: int 0: Success, 1: Error, 2: Skipped: File exists
    """
    fullPath = fileName
    if len(filePath) > 0:
        fullPath = filePath + "/" + fileName
        # Create outPath directory if not exists
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    # Save file in outPath if it doesn't exist yet
    if overwrite or (not os.path.exists(fullPath)):
        try:
            with open(fullPath, "wb+") as file:
                file.write(response.content)
            return 0

        except Exception:
            return -1
    else:
        return -2


def _formatSize(size: float):
    """
    Returns a formatted file size string representation
    @param size: {float} Size in bytes
    """
    return humanize.naturalsize(size)


def _formatDuration(secs: float):
    """
    Returns a formatted time duration string representation of a duration in seconds
    @param seconds: float
    """
    if secs < 1.0:
        txtDownTime = f"{secs:.3f} seconds"
    else:
        d = timedelta(seconds=secs)
        txtDownTime = humanize.naturaldelta(d)

    return txtDownTime


def _printErrorMessage(response):
    """
    Method to print infromation of an error returned by the API to the console
    Builds the error description from the response object
    """
    status = response.status_code
    if status == 400:
        print(f"\nError 400 - Bad Request: {response.url}")
        payload = response.json()
        if len(payload) >= 1:
            for e in payload["errors"]:
                code = e["errorCode"]
                msg = e["errorMessage"]
                parameters = e["parameter"]
                print(f"   Error {code}: {msg} (parameter: {parameters})")

    elif status == 401:
        print(
            f"Error 401 - Unauthorized: {response.url}\n"
            "Please check that your Web Services API token is valid.",
            "Find your token in your registered profile at https://data.oceannetworks.ca.",
        )

    else:
        msg = f"\nError {status} - {response.reason}\n"
        print(msg)


def _messageForError(status: int):
    """
    Return a description string for an HTTP error code
    """
    errors = {
        500: "Internal server error",
        503: "Service temporarily unavailable",
        598: "Network read timeout error",
    }
    return errors[status]
