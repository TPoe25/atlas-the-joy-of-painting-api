#!/usr/bin/env python3
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

print("Starting ETL")

os.system("python3 scripts/parse_paintings.py")
os.system("python3 scripts/parse_dates.py")
os.system("python3 scripts/parse_elements.py")

print("ETL completed successfully")
