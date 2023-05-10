#!/usr/bin/env sh

. .venv/bin/activate
pip-sync ./dev-requirements.txt ./requirements.txt
