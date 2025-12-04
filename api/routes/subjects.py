#!/usr/bin/env python3
from flask import Blueprint, jsonify
from api.db import get_connection

subjects_blueprint = Blueprint("subjects", __name__, url_prefix="/subjects")

@subjects_blueprint.get("/")
def get_subjects():
    """Returns a list of all subjects."""
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT id, name FROM subjects ORDER BY name ASC")
    rows = cursor.fetchall()

    db.close()

    return jsonify([{"id": row[0], "name": row[1]} for row in rows])

