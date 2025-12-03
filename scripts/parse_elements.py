#!/bin/env python3
import csv
from typing import Dict
from helpers.clean_title import clean_title

# Attempt to import psycopg2 but handle if it's not installed so static checkers won't crash.
try:
    import psycopg2
except Exception:
    psycopg2 = None  # runtime will raise a clear error if used without the package

# Create a database connection
DB_NAME = "the_joy_of_painting"
ELEMENTS_FILE = "data/episode_elements.csv"

def load_elements():
    """ Loads episode elements from a CSV file into the database."""

    if psycopg2 is None:
        raise ImportError("psycopg2 is required to run this function; you installed it doublecheck -- says it was a pylance not runtime error when looking up info about this")

    connection = psycopg2.connect(dbname=DB_NAME)
    cursor = connection.cursor()

    with open(ELEMENTS_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []

        # Determine which columns represent subjects/elements (skip EPISODE and TITLE)
        subject_columns = [col for col in fieldnames if col not in ("EPISODE", "TITLE")]

        # Ensure all subjects exist in the subjects table, using lowercase names
        subject_names = [s.lower() for s in subject_columns]
        for name in subject_names:
            cursor.execute("""
                INSERT INTO subjects (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (name,))
        # Build a mapping of subject name -> id for fast lookups
        subject_id_map: Dict[str, int] = {}
        if subject_names:
            cursor.execute(
                "SELECT id, name FROM subjects WHERE name = ANY(%s);",
                (subject_names,)
            )
            for sid, name in cursor.fetchall():
                subject_id_map[name] = int(sid)
                subject_id_map[name] = sid

        # Rewind and recreate the reader so iteration starts at the first data row
        file.seek(0)
        reader = csv.DictReader(file)

        for row in reader:
            title = clean_title(row.get("TITLE", ""))

            cursor.execute("SELECT id FROM episodes WHERE title = %s", (title,))
            episode = cursor.fetchone()

            if not episode:
                continue

            episode_id = episode[0]

            for subject in subject_columns:
                # treat a "1" in the CSV as presence of the subject/element
                if row.get(subject) == "1":
                    name = subject.lower()
                    subject_id = subject_id_map.get(name)
                    if subject_id is None:
                        # If the subject wasn't found for some reason, skip it
                        continue

                    # Ensure subject_id has a concrete int type for the DB driver / type checkers
                    subject_id = int(subject_id)

                    cursor.execute("""
                        INSERT INTO episode_subjects (episode_id, subject_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (episode_id, subject_id))

    connection.commit()
    cursor.close()
    connection.close()


