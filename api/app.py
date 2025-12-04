#!/usr/bin/env python3
from flask import Flask, jsonify, Blueprint
from routes.episodes import episodes_blueprint
from routes.colors import colors_blueprint
from routes.subjects import subjects_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(episodes_blueprint)
app.register_blueprint(colors_blueprint)
app.register_blueprint(subjects_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
    """Starts the Flask API server."""
