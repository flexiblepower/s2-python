#!/bin/bash


. .venv/bin/activate
datamodel-codegen --input specification/openapi.yml --input-file-type openapi --output src/s2python/generated/gen_s2.py
