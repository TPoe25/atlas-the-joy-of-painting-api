#!/usr/bin/env python3
import csv
import psycopg2 # for PostgreSQL database connectivity/ installed
from clean_title import clean_title

# Create a database connection
DB_NAME = "the_joy_of_painting"
PAINTINGS_FILE = "data/bob_ross_paintings.csv"

def load_paintings():
    """Loads painting data from a CSV file into the database."""

    try:
        connection = psycopg2.connect(dbname=DB_NAME)
        cursor = connection.cursor()
    except Exception as error:
        print(f"Error connecting to database", error)
        return

    try:
        with open(PAINTINGS_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                title_clean = clean_title(row.get("painting_title"))
                season_number = int(row.get("season"))
                episode_number = int(row.get("episode"))
                img_url = row.get("img_src")
                youtube_url = row.get("youtube_src")

                # insert the edited data into the database
                cursor.execute("""
                    INSERT INTO episodes (title, season, episode, img_url, youtube_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (title) DO NOTHING;
                """, (
                    title_clean,
                    season_number,
                    episode_number,
                    img_url,
                    youtube_url,
                ))

                # get episode id
                cursor.execute("SELECT id FROM episodes WHERE title = %s", (title_clean,))
                result = cursor.fetchone()

                if not result:
                    print(f"Failed to retrieve episode ID for title: {title_clean}")
                    continue

                ep_id = result[0]

                try:

                    # parse through color arrays and insert into database
                    color_list = eval(row["colors"])
                    hex_list = eval(row["hex_colors"])

                except Exception:
                    print(f"Failed to parse color arrays for title: {title_clean}")
                    continue

                for color_name, hex_value in zip(color_list, hex_list):
                    color_name = color_name.strip()

                    cursor.execute("""
                        INSERT INTO colors (name, hex)
                        VALUES (%s, %s)
                        ON CONFLICT (name) DO NOTHING;
                    """, (color_name, hex_value))

                    cursor.execute("SELECT id FROM colors WHERE name = %s", (color_name,))
                    color = cursor.fetchone()

                    if not color:
                        continue

                    color_id = color[0]

                    # insert episode-color relationship into database
                    cursor.execute("""
                        INSERT INTO episode_colors (episode_id, color_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (ep_id, color_id))

                # commit changes
        connection.commit()

    except Exception as error:
        print(f"Error loading painting data", error)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_paintings()
    """Loads painting data from a CSV file into the database."""
