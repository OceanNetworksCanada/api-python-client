import os
from pathlib import Path

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

    @staticmethod
    def update_file_with_token_and_qa(tmp_py: Path) -> None:
        """
        Modify tmp_py inplace to test against QA environment with the correct token .

        Assume that tmp_py initiate onc object with a dummy "YOUR_TOKEN" argument.
        """
        with open(tmp_py) as f:
            contents = f.readlines()
        index = contents.index('onc = ONC("YOUR_TOKEN")\n')
        contents.insert(
            index + 1,
            f"onc.token, onc.production, onc.timeout = '{token}', False, 300\n",  # noqa: E501
        )
        with open(tmp_py, "w") as f:
            f.writelines(contents)
