from typing import List
from requests import Response
from time import time
from decimal import Decimal

class _PollLog:
    """
    A helper for DataProductFile
    Keeps track of the messages printed in a single product download process
    """
    def __init__(self, showInfo: bool):
        """
        @param showInfo same as in parent ONC object
        """
        self._messages = []       # unique messages returned during the product order
        self._runStart = 0.0      # {float} timestamp (seconds)
        self._runEnd   = 0.0
        self._showInfo = showInfo # flag for writing console messages
        self._doPrintFileCount = True
        self._lastPrintedDot   = False # True after printing a dot (.) without a newline


    def logMessage(self, response):
        """
        Adds a message to the messages list if it's new
        Prints message to console, or "." if it repeats itself
        """
        # Detect if the response comes from a "run" or "download" method
        origin = 'download'
        if isinstance(response, list) and 'status' in response[0]:
            origin = 'run'

        # Store and print message
        if origin == 'run':
            msg = response[0]['status']
        else:
            if 'message' in response:
                msg = response['message']
            else:
                msg = 'Generating'
        
        if not self._messages or msg != self._messages[-1]:
            # Detect and print change in the file count
            if origin == 'run': 
                fileCount = response[0]['fileCount']
                if self._doPrintFileCount and fileCount > 0:
                    self.printInfo('\n   {:d} files generated for this data product'.format(fileCount), True)
                    self._doPrintFileCount = False

            self._messages.append(msg)
            self.printInfo('\n   ' + msg, sameLine=True)
        else:
            self.printInfo('.', sameLine=True)


    def printInfo(self, msg: str, sameLine: bool = False):
        """
        Conditional printing helper
        """
        self._lastPrintedDot = (msg == '.')

        if self._showInfo:
            if sameLine:
                print(msg, end="", flush=True)
            else:
                print(msg)


    def printNewLine(self):
        '''
        Prints a line break only if the last message printed was a dot (.)
        '''
        if self._lastPrintedDot:
            print('')