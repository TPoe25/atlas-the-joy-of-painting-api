#!/usr/bin/env python3
import os

print("Starting ETL")

os.system("python3 scripts/parse_paintings.py")
os.system("python3 scripts/parse_elements.py")
os.system("python3 scripts/parse_dates.py")

print("ETL completed successfully")
