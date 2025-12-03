#!/bin/env python3
import csv
import psycopg2
from clean_title import clean_title

# Create a database connection
DB_NAME = "the_joy_of_painting"

def load_elements():
    """ Loads episode elements from a CSV file into the database."""

    try:
        connection = psycopg2.connect(dbname=DB_NAME)
    except Exception as error:
        print(f"Error connecting to database", error)
        return

    cursor = connection.cursor()
