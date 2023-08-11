#!/usr/bin/env sh

. .venv/bin/activate
pip-compile -U --resolver=backtracking -o ./requirements.txt ./requirements.in
pip-compile -U --resolver=backtracking -o ./dev-requirements.txt ./dev-requirements.in
