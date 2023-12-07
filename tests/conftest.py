import os

import pytest
from dotenv import load_dotenv

from onc import ONC

load_dotenv(override=True)
token = os.getenv("TOKEN")
is_prod = os.getenv("ONC_ENV", "PROD") == "PROD"


@pytest.fixture
def requester(tmp_path) -> ONC:
    return ONC(token, is_prod, outPath=tmp_path)
