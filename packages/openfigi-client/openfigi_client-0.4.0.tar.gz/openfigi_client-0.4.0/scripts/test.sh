#!/usr/bin/env bash

set -e

coverage run -m pytest -m 'not slow'
coverage report
coverage xml
