# Project
- This project is a library, not an application. It is intended to be used as a dependency in other projects.
- This project defines a python version for the S2 network protocol.
- We use semantic versioning for this project. The version number is defined in `pyproject.toml` and should be updated with each release.
- Our interface to users is:
  - Message definitions for the S2 network protocol that live in `s2python/{common,ddbc,frbc,ombc,pebc,ppbc}/.`
    - We use an openapi specification to generate the message definitions. The generated code is in `s2python/generated`.
      - We do not alter generated code manually. If we need to change the generated code, we change the openapi specification and regenerate the code.
      - The openapi specifications lives in `specification/` and is based on the official `s2-json` repository.
  - Connection classes that run on top of some Medium (e.g. TCP, UDP, WebSocket, etc.) and handle the S2 network protocol that live in `s2python/connection/`.
  - Standard medium definitions for websocket and other connections that live in `s2python/connection/{async_,sync}/medium`.
  - Example scripts under the `examples/` folder.

# Python
- We use Python 3.9 as the earliest python to support.
- We use Python 3.14 as the latest python to support.

# Poetry
- This is a library, do not pin any dependencies in pyproject.toml that break dependency management for downstream users.
  - Feel free to use a pin that defines a minimum version of a dependency, but do not pin to a specific version.
- `poetry.lock` is checked in to the repository to ensure reproducible builds for development and testing but this is NOT the same environment users use.

# Development
- You have development tooling available under `ci/` that you can use to run linters, formatters, type checkers, and unit tests:
  - `lint.sh`: Run the linters and formatters.
  - `test_unit.sh`: Run the unit tests.
  - `typecheck.sh`: Run the type checkers.
  - `update_dependencies.sh`: Update dependencies in poetry.lock based on pyproject.toml.
  - `generate_s2.sh`: Generate the S2 message definitions from the openapi specification.
  - `clean.sh`: Remove all generated files and build artifacts that are not in the git tree but locally available.
  - `setup_dev_environment.sh`: Set up the development environment with an initial virtual environment. Dependencies still need to be installed with `install_dependencies.sh`.
  - `install_dependencies.sh`: Install dev dependencies in the virtual environment.
- Library source lives under `src/s2python`.

# Unit Testing
- Use `ci/test_unit.sh` directly for unit testing instead of `python -m pytest`.
- Use #Arrange, # Act, #Assert comments to separate the three phases of a unit test.
- Test only one function per test file. If a function has multiple behaviors, create multiple test files for that function.
- Use `pytest.mark.parametrize` to test multiple inputs and outputs for a single function if it simplifies code and reduces duplication.
  - Do not overcomplicate. If parametrize leads to a test that is hard to read, break it into multiple tests instead.
- Unit tests live under `tests/unit/`.
  - Mimic the folder structure under `src.`
- Unit test functions should be named according to `test__<function under test>__<behavior being tested>`.
- Unit tests should use type hints as well.

# Typehinting
- Use `ci/typecheck.sh` for type checking.
- We want to satisfy both pyright and mypy.
