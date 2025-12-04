#!/bin/env python3
import re
import psycopg2
from helpers.clean_title import clean_title
from datetime import datetime

DB_NAME = "the_joy_of_painting"
DATE_FILE = "data/TJOP-Episode_Dates.txt"

pattern = r'"(.+?)"\s*\(([^)]+)\)'

def load_dates():
    connection = psycopg2.connect(dbname=DB_NAME)
    cursor = connection.cursor()

    with open(DATE_FILE, encoding="utf-8") as file:
        index = 0  # track which line we are on

        for line in file:
            match = re.search(pattern, line)
            if not match:
                continue

            title = match.group(1)
            date_string = match.group(2)

            # Parse the date
            try:
                air_date = datetime.strptime(date_string, "%B %d, %Y")
            except Exception:
                print("Failed to parse:", title, date_string)
                continue

            month = air_date.month

            # Calculate season + episode number
            season = (index // 13) + 1
            episode = (index % 13) + 1
            index += 1

            # Update by season + episode, not title
            cursor.execute("""
                UPDATE episodes
                SET air_date = %s, month_of_air = %s
                WHERE season = %s AND episode = %s;
            """, (air_date, month, season, episode))

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    load_dates()
    """Loads episode dates from a CSV file into the database."""
