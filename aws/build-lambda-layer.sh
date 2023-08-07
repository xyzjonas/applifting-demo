#!/bin/bash

set -e

poetry install
poetry build

pip install \
  --target=python \
  --implementation cp \
  --python 3.10 \
  --only-binary=:all: \
  --upgrade \
  psycopg[binary]

pip install \
  --target=python \
  --python 3.10 \
  --only-binary=:all: \
  psycopg

pip install \
  --target=python \
  --implementation cp \
  --python 3.10 \
  --only-binary=:all: \
  --upgrade \
  ./dist/*.whl


zip -r ./dist/lambda-layer.zip python
rm -rf python
