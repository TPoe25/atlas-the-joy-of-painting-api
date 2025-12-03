#!/bin/env python3
import re
import psycopg2 # for PostgreSQL database connectivity/installed
from helpers.clean_title import clean_title
from datetime import datetime

# Create a database connection
DB_NAME = "the_joy_of_painting"
DATE_FILE = "data/episode_dates.csv"

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

            raw_title = match.group(1)
            date_string = match.group(2)

            title_clean = clean_title(raw_title)
            air_date = datetime.strptime(date_string, "%B %d, %Y") # format: Month Day, Year
            month = air_date.month

            cursor.execute("""
                UPDATE episodes
                SET air_date = %s, month_of_air = %s;
            """, (air_date, month, title_clean))

    connection.commit()
    cursor.close()
    connection.close()
