#!/bin/bash
# Runs the entire test suite locally.
#
# To run a specific command:
#
#   tox -c tox-full.ini -- -s burlap/tests/test_common.py::CommonTests::test_iter_sites
#
set -e
[ -d .env ] && rm -Rf .env
virtualenv .env
. .env/bin/activate
pip install -r requirements-test.txt
./pep8.sh
rm -Rf ./burlap/*.pyc
time tox -c tox-full.ini
