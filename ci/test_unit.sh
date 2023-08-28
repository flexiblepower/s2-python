#!/usr/bin/env sh

. .venv/bin/activate
PYTHONPATH="$PYTHONPATH:src/" pytest --cov=s2python --cov-report=html:./unit_test_coverage/ -v tests/unit/
