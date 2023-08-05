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

#pip install \
#  --platform manylinux2014_x86_64 \
#  --target=python \
#  --python 3.10 \
#  --only-binary=:all: \
#  psycopg2

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


zip -r lambda-layer.zip python
