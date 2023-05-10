#!/usr/bin/env sh

. .venv/bin/activate
python -m piptools compile --resolver=backtracking -o ./requirements.txt ./requirements.in
python -m piptools compile --resolver=backtracking -o ./dev-requirements.txt ./dev-requirements.in
