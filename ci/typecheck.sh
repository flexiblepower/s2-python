#!/usr/bin/env sh

. .venv/bin/activate
python -m mypy ./s2_analyzer_backend/ ./test/
