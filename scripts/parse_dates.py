#!/bin/env python3
import re
import psycopg2 # for PostgreSQL database connectivity/installed
from helpers.clean_title import clean_title
from datetime import datetime

# Create a database connection
DB_NAME = "the_joy_of_painting"
DATE_FILE = "data/TJOP-Episode_Dates.txt"

# Regular expression to extract season and episode numbers from the title
pattern = r'"(.+?)" \((.+?)\)'

def load_dates():
    """Loads episode dates from a CSV file into the database."""

    connection = psycopg2.connect(dbname=DB_NAME)
    cursor = connection.cursor()

    with open(DATE_FILE, encoding="utf-8") as file:
        for line in file:
            match = re.search(pattern, line)
            if not match:
                continue

            cleaned_title = clean_title(match.group(1))

            date_string = match.group(2)

            try:
                air_date = datetime.strptime(date_string, "%B %d, %Y") # format: Month Day, Year
            except Exception:
                print("Failed to parse:", cleaned_title, date_string)
                continue

            month = air_date.month

            cursor.execute("""
                UPDATE episodes
                SET air_date = %s, month_of_air = %s
                WHERE title = %s;
            """, (air_date, month, cleaned_title))

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    load_dates()
    """Loads episode dates from a CSV file into the database."""
