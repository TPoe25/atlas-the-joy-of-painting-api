#!/usr/bin/env python3
import csv
import psycopg2
from clean_title import clean_title

# Create a database connection
DB_NAME = "the_joy_of_painting"

def load_paintings():
    """Loads painting data from a CSV file into the database."""

    conn = psycopg2.connect(dbname=DB_NAME)
    cur = conn.cursor()

    with open("data/bob_ross_paintings.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            title = clean_title(row["painting_title"])
            season = int(row["season"])
            episode = int(row["episode"])
            img = row.get("img_src")
            yt = row.get("youtube_src")

            # imsert the edited data into the database
            cur.execute("""
                INSERT INTO episodes (title, season, episode, img_url, youtube_url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (title) DO NOTHING;
            """, (title, season, episode, img, yt))

            # get episode id
            cur.execute("SELECT id FROM episodes wHERE title = %s", (title,))
            ep_id = cur.fetchone()[0]

            # parse through color arrays and insert into database
            color_list = eval(row["colors"])  # convert string representation of list to actual list
            hex_list = eval(row["hex_colors"]) # convert string representation of list to actual list

            for color_name, hex_value in zip(color_list, hex_list):
                color_name = color_name.strip()

                cur.execute("""
                    INSERT INTO colors (name, hex)
                    VALUES (%s, %s)
                    ON CONFLICT (name) DO NOTHING;
                """, (color_name, hex_value))

                cur.execute("SELECT id FROM colors WHERE name = %s", (color_name,))
                color_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO episode_colors (episode_id, color_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (episode_id, color_id))

    conn.commit()
    conn.close()
    print("Paintings loaded successfully.")

if __name__ == "__main__":
    load_paintings()
    """Loads painting data from a CSV file into the database."""
