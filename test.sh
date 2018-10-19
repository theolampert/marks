#!/bin/bash
flake8
python3 src/test.py
rm ./__test.db
