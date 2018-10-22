#!/bin/bash
flake8
python3 ./src/test.py -v
rm ./__test.db
