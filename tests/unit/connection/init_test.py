"""Tests that s2python.connection does not require the optional 'websockets' dependency."""

import os
import subprocess
import sys

import pytest

SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "src")


def _run_without_websockets(code: str) -> subprocess.CompletedProcess[str]:
    # Setting sys.modules['websockets'] to None makes any import of it raise ImportError.
    script = "import sys\nsys.modules['websockets'] = None\n" + code
    python_path = [SRC_DIR]
    if os.environ.get("PYTHONPATH"):
        python_path.append(os.environ["PYTHONPATH"])
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(python_path))
    return subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, env=env, check=False
    )


@pytest.mark.parametrize(
    "import_statement",
    [
        "import s2python.connection",
        "from s2python.connection import AssetDetails",
        "import s2python.connection.async_",
        "import s2python.connection.sync",
        "from s2python.connection.async_.control_type.class_based import OMBCControlType",
        "from s2python.connection.sync.control_type.class_based import OMBCControlType",
    ],
)
def test__import__works_without_websockets(import_statement: str) -> None:
    # Arrange
    code = import_statement + "\nassert 's2python.connection.async_.medium.websocket' not in sys.modules\n"

    # Act
    result = _run_without_websockets(code)

    # Assert
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "import_statement",
    [
        "from s2python.connection.quickstarts import BlockingWebsocketClientRM",
        "from s2python.connection.async_.medium.websocket import WebsocketClientMedium",
    ],
)
def test__import__websocket_modules_require_websockets(import_statement: str) -> None:
    # Arrange
    code = import_statement

    # Act
    result = _run_without_websockets(code)

    # Assert
    assert result.returncode != 0
    assert "The 'websockets' package is required" in result.stderr
