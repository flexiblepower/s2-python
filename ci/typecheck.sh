#!/usr/bin/env sh

. .venv/bin/activate
mypy --config-file mypy.ini src/ ./tests/unit/ examples/
pyright
