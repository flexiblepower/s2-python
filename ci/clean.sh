. .venv/bin/activate

tox -e clean
rm -Rf .pytest_cache/ .tox/ dist/ src/*.egg-info/ unit_test_coverage/ .coverage
