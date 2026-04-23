from onc.modules._Messages import setup_logger


class _PollLog:
    """
    A helper for DataProductFile
    Keeps track of the messages printed in a single product download process
    """

    def __init__(self, verbosity: str):
        """
        Parameters
        ----------
        verbosity : str
            Standard logging level string.
        """
        self._messages = []  # unique messages returned during the product order
        self._runStart = 0.0  # {float} timestamp (seconds)
        self._runEnd = 0.0
        self._verbosity = verbosity
        self._log = setup_logger("onc.poll", level=verbosity)
        self._doLogFileCount = True

    def logMessage(self, response):
        """
        Adds a message to the messages list if it's new
        Logs message to logger
        """
        # Detect if the response comes from a "run" or "download" method
        origin = "download"
        if isinstance(response, list) and "status" in response[0]:
            origin = "run"

        # Store and print message
        if origin == "run":
            msg = response[0]["status"]
        else:
            msg = response.get("message", "Generating")

        if not self._messages or msg != self._messages[-1]:
            # Detect and print change in the file count
            if origin == "run":
                fileCount = response[0]["fileCount"]
                if self._doLogFileCount and fileCount > 0:
                    self._log.info(
                        f"   {fileCount} files generated for this data product"
                    )
                    self._doLogFileCount = False

            self._messages.append(msg)
            self._log.info("   " + msg)
        else:
            # For repeating messages, log at DEBUG level to avoid cluttering INFO logs
            self._log.debug(msg)

    def printNewLine(self):
        """
        Deprecated. Newlines are handled by the logger.
        """
        pass
