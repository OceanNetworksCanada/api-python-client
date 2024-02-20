import os

import pytest
from dotenv import load_dotenv
from onc import ONC

load_dotenv(override=True)
token = os.getenv("TOKEN")
is_prod = os.getenv("ONC_ENV", "PROD") == "PROD"


def pytest_configure():
    print("========== ONC config ==========")
    print(f"Testing environment: {'PROD' if is_prod else 'QA'}")


@pytest.fixture
def requester(tmp_path) -> ONC:
    return ONC(token, is_prod, outPath=tmp_path)


@pytest.fixture(scope="session")
def util():
    return Util


class Util:
    @staticmethod
    def get_download_files_num(onc: ONC) -> int:
        return len(list(onc.outPath.iterdir()))

    @staticmethod
    def assert_dict_key_types(data: dict, expected_keys: dict) -> None:
        for key, val_type in expected_keys.items():
            assert key in data
            if val_type is None:
                assert data[key] is None
            else:
                assert isinstance(data[key], val_type)
