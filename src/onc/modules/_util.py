from datetime import timedelta
from pathlib import Path

import humanize
import requests


def saveAsFile(
    response: requests.Response, outPath: Path, fileName: str, overwrite: bool
) -> None:
    """
    Saves the file downloaded in the response object, in the outPath, with filename
    If overwrite, will overwrite files with the same name
    """
    filePath = outPath / fileName
    outPath.mkdir(parents=True, exist_ok=True)

    # Save file in outPath if it doesn't exist yet
    if Path.exists(filePath) and not overwrite:
        raise FileExistsError(filePath.resolve())
    with open(filePath, "wb+") as file:
        file.write(response.content)


def _formatSize(size: float) -> str:
    """
    Returns a formatted file size string representation
    @param size: {float} Size in bytes
    """
    return humanize.naturalsize(size)


def _formatDuration(secs: float) -> str:
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


def _createErrorMessage(response: requests.Response) -> str:
    """
    Method to print infromation of an error returned by the API to the console
    Builds the error description from the response object
    """
    status = response.status_code
    if status == 400:
        prefix = f"\nStatus 400 - Bad Request: {response.url}"
        payload = response.json()
        # see https://wiki.oceannetworks.ca/display/O2A for error codes
        msg = f"{prefix}\n" + "\n".join(
            [
                f"API Error {e['errorCode']}: {e['errorMessage']} "
                f"(parameter: {e['parameter']})"
                for e in payload["errors"]
            ]
        )
        return msg

    elif status == 401:
        return (
            f"Status 401 - Unauthorized: {response.url}\n"
            "Please check that your Web Services API token is valid. "
            "Find your token in your registered profile at "
            "https://data.oceannetworks.ca."
        )
    else:
        return f"The server request failed with HTTP status {status}."
