#!/usr/bin/env sh

set -e
. .venv/bin/activate
pylint src/ examples/
PYTHONPATH="src:$PYTHONPATH" pylint --disable=protected-access,invalid-overridden-method tests/unit/
