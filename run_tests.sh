#!/bin/bash
export PYTHONPATH=$PYTHONPATH:src
python3 -m pytest tests/
