import logging
import re
import requests
import time

REQ_MSG = "Requested: {}"  # get request url
RESPONSE_TIME_MSG = "Response received in {} seconds." # requests.elapsed value.
RESPONSE_MSG = "HTTP Response: {} ({})" # Brief description, status code
MULTIPAGE_MSG = ("The requested data quantity is greater than the "
                 "supplied row limit and will be downloaded over multiple requests.")


def setup_logger(logger_name: str = 'onc-client',
                 level: int | str = 'DEBUG') -> logging.Logger:
    """
    Set up a logger object for displaying verbose messages to console.

    :param logger_name: The unique logger name to use. Can be shared between modules
    :param level: The logging level to use. Default is 2, which corresponds to DEBUG.
    :return: The configured logging.Logger object.
    """

    logger = logging.getLogger(logger_name)
    logger.propagate = False
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console.setLevel(level)

        # Set the logging format.
        dtfmt = '%Y-%m-%dT%H:%M:%S'
        strfmt = f'%(asctime)s.%(msecs)03dZ | %(name)-12s | %(levelname)-8s | %(message)s'
        #strfmt = f'%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(message)s' # Use this if you don't want to include logger name.
        fmt = logging.Formatter(strfmt, datefmt=dtfmt)
        fmt.converter = time.gmtime

        console.setFormatter(fmt)
        logger.addHandler(console)
    return logger


def scrub_token(input: str) -> str:
    """
    Replace a token in a query URL or other string with the string 'REDACTED'
    so that users don't accidentally commit their tokens to public repositories
    if ONC Info/Warnings are too verbose.

    :param query_url: An Oceans 3.0 API URL or string with a token query parameter.
    :return: A scrubbed url.
    """
    token_regex = r'(&token=[a-f0-9-]{36})'
    token_qp = re.findall(token_regex, input)[0]
    redacted_url = input.replace(token_qp, '&token=REDACTED')
    return redacted_url


def build_error_message(response: requests.Response, redact_token: bool) -> str:
    """
    Build an error message from a requests.Response object.

    :param response: A requests.Response object.
    :param redact_token: If true, redact tokens before returning an error message.
    :return: An error message.
    """
    payload = response.json()
    if 'message' in payload.keys():
        message = payload['message']
    else:
        message = None

    if 'errors' in payload.keys():
        errors = payload['errors']
        error_messages = []
        for error in errors:
            emsg = (f"(API Error Code {error['errorCode']}) "
                    f"{error['errorMessage']} for query parameter(s) "
                    f"'{error['parameter']}'.")
            error_messages.append(emsg)
        error_message = '\n'.join(error_messages)
    else:
        error_message = None
    msg = '\n'.join([m for m in (message, error_message) if m is not None])
    if redact_token is True and 'token=' in msg:
        msg = scrub_token(msg)
    return msg

