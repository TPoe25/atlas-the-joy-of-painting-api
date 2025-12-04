#!/usr/bin/env python3
from flask import Blueprint, request, jsonify
from api.db import get_connection

episodes_blueprint = Blueprint("episodes", __name__, url_prefix="/episodes")

@episodes_blueprint.get("/")
def get_episodes():
    """Returns a list of all episodes."""
    db = get_connection()
    cursor = db.cursor()

    # Incoming filter parameters
    month = request.args.get("month")
    colors = request.args.get("colors")
    subjects = request.args.get("subjects")
    mode = request.args.get("mode", "all").lower()

    colors_list = [c.strip() for c in colors.split(",")] if colors else []
    subjects_list = [s.strip() for s in subjects.split(",")] if subjects else []

    # Base query
    query = """
        SELECT ep.id, ep.title, ep.season, ep.episode, ep.img_url, ep.youtube_url,
               ep.air_date, ep.month_of_air
        FROM episodes ep
    """

    where_clauses = []
    parameters = []

    # Filter: Month
    if month:
        where_clauses.append("ep.month_of_air = %s")
        parameters.append(int(month))

    # AND / OR grouping logic
    joiner = " AND " if mode == "all" else " OR "

    # Filter: Subjects
    if subjects_list:
        where_clauses.append("""
            ep.id IN (
                SELECT episode_id
                FROM episode_subjects es
                JOIN subjects s ON s.id = es.subject_id
                WHERE s.name = ANY(%s)
            )
        """)
        parameters.append(subjects_list)

    # Filter: Colors
    if colors_list:
        where_clauses.append("""
            ep.id IN (
                SELECT episode_id
                FROM episode_colors ec
                JOIN colors c ON c.id = ec.color_id
                WHERE c.name = ANY(%s)
            )
        """)
        parameters.append(colors_list)

    # Assemble WHERE clause
    if where_clauses:
        query += " WHERE " + joiner.join(where_clauses)

    cursor.execute(query, parameters)
    episodes = cursor.fetchall()

    # Build JSON response
    response_list = []

    for ep in episodes:
        episode_id = ep[0]

        # Fetch colors for this episode
        cursor.execute("""
            SELECT c.name
            FROM colors c
            JOIN episode_colors ec ON ec.color_id = c.id
            WHERE ec.episode_id = %s
        """, (episode_id,))
        ep_colors = [row[0] for row in cursor.fetchall()]

        # Fetch subjects for this episode
        cursor.execute("""
            SELECT s.name
            FROM subjects s
            JOIN episode_subjects es ON es.subject_id = s.id
            WHERE es.episode_id = %s
        """, (episode_id,))
        ep_subjects = [row[0] for row in cursor.fetchall()]

    # Format results into a JSON response
    response_list = []
    for ep in episodes:
        episode_id = ep[0]

        # get colors and subjects associated with the episode
        cursor.execute("""
            SELECT c.name
            FROM colors c
            JOIN episode_colors ec ON ec.color_id = c.id
            WHERE ec.episode_id = %s
        """, (episode_id,))
        ep_colors = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT s.name
            FROM subjects s
            JOIN episode_subjects es ON es.subject_id = s.id
            WHERE es.episode_id = %s
        """, (episode_id,))
        ep_subjects = [row[0] for row in cursor.fetchall()]

        response_list.append({
            "id": ep[0],
            "title": ep[1],
            "season": ep[2],
            "episode": ep[3],
            "img_url": ep[4],
            "youtube_url": ep[5],
            "air_date": ep[6],
            "month_of_air": ep[7],
            "colors": ep_colors,
            "subjects": ep_subjects
        })

    db.close()
    return jsonify(response_list)
