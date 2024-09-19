#!/usr/bin/env bash

set -e

uv build
uvx twine upload dist/*
