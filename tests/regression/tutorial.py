import runpy
import subprocess
from pathlib import Path


def test_onc_library_tutorial(tmp_path, util):
    notebook = (
        Path(__file__).parent.parent.parent
        / "doc/source/Tutorial/onc_Library_Tutorial.ipynb"
    )
    tmp_py = tmp_path / notebook.with_suffix(".py").name

    # Convert jupyter file to py file in a tmp directory
    subprocess.run(["jupytext", "--output", tmp_py, notebook])

    util.update_file_with_token_and_qa(tmp_py)

    runpy.run_path(tmp_py.resolve().as_posix())
