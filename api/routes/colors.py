#!/usr/bin/env python3
from flask import Blueprint, jsonify
from api.db import get_connection

colors_blueprint = Blueprint("colors", __name__, url_prefix="/colors")

@colors_blueprint.get("/")
def get_colors():
    """Returns a list of all colors."""
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT id, name FROM colors ORDER BY name ASC")
    rows = cursor.fetchall()

    db.close()

    return jsonify([{"id": row[0], "name": row[1]} for row in rows])

