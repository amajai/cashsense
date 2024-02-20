#!/usr/bin/python3
"""Entry point for the application"""
from api import app, app_views

app.register_blueprint(app_views)


if __name__ == "__main__":
    app.run(debug=True)