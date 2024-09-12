#!/usr/bin/env sh

. .venv/bin/activate
pylint src/ tests/unit/ examples/
