#!/usr/bin/env sh

. .venv/bin/activate
status=0
mypy --config-file mypy.ini src/ ./tests/unit/ examples/ || status=1
pyright || status=1
exit "$status"
