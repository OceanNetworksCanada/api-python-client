import runpy
import os

from pathlib import Path

import pytest

from onc import ONC
is_prod = os.getenv("ONC_ENV", "PROD") == "PROD"

env_script = Path(__file__).parent.parent.resolve() / "libraries" / "env_variable.py"
runpy.run_path(env_script)


@pytest.fixture
def requester(tmp_path) -> ONC:
    return ONC(os.environ["TOKEN"], is_prod, outPath=tmp_path)
