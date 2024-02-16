"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, Response, request, jsonify

from date_functions import convert_to_datetime, get_day_of_week_on, get_days_between

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome message."""
    return jsonify({ "message": "Welcome to the Days API." })


@app.route("/between", methods =["POST"])
def get_between():
    """Returns the number of days between two dates"""
    try:
        first = convert_to_datetime(request.json["first"])
        last = convert_to_datetime(request.json["last"])
    except:
        return jsonify({'error': True,
                        'message': 'Could not convert to datetime, check format.'}), 400
    return jsonify({ "days": get_days_between(first, last)}), 200


@app.route("/weekday", methods =["POST"])
def get_weekday():
    """Returns the day of the week a specific date is"""
    try:
        first = convert_to_datetime(request.json["date"])
    except:
        return jsonify({'error': True,
                        'message': 'Could not convert to datetime, check format.'}), 400
    return jsonify({ "weekday": get_day_of_week_on(first)}), 200

if __name__ == "__main__":
    app.run(port=8080, debug=True)
