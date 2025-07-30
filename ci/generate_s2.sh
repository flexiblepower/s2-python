#!/bin/bash


. .venv/bin/activate
datamodel-codegen  --input specification/openapi.yml --input-file-type openapi --output-model-type pydantic_v2.BaseModel --output src/s2python/generated/gen_s2.py --use-one-literal-as-default --use-subclass-enum --output-datetime-class AwareDatetime --use-double-quotes
