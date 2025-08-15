#!/bin/bash
pip install -r requirements-test.txt
export PYTHONPATH=$PYTHONPATH:src
python3 -m pytest tests/
