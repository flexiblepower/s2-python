#!/usr/bin/env sh

. .venv/bin/activate
pip-compile --extra=ws --extra=fastapi --extra=development --extra=docs --extra=testing --output-file=./dev-requirements.txt pyproject.toml
