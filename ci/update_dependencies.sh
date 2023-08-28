#!/usr/bin/env sh

. .venv/bin/activate
pip-compile -U --extra=testing --extra=development --extra=docs -o ./dev-requirements.txt  setup.cfg
