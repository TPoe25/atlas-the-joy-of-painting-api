#!/usr/bin/env python3
import psycopg2 # for PostgreSQL database connectivity/ installed
import os # for accessing environment variables

# Create a database connection
DB_NAME = "the_joy_of_painting"

def get_connection():
    try:
        return psycopg2.connect(dbname=DB_NAME)
    except Exception as error:
        print("Error connecting to database:", error)
        return None
