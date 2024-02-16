"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, request, jsonify

from date_functions import convert_to_datetime, get_day_of_week_on, get_days_between



app = Flask(__name__)
app_history = []
print(app_history )

def add_to_history(current_request: list) -> None:
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index() -> list:
    """Returns an API welcome message."""
    add_to_history(request)
    return jsonify({ "message": "Welcome to the Days API." })


@app.route("/between", methods =["POST"])
def between() -> list:
    """Returns the number of days between two dates"""
    if request.method == "POST":
        add_to_history(request)
        if "first" not in request.json or "last" not in request.json:
            return jsonify({"error": "Missing required data."}), 400
        first = request.json["first"]
        last = request.json["last"]
        if not isinstance(first, str) or not isinstance(first, str):
            return jsonify({'error': 'Unable to convert value to datetime.'}), 400
        try:
            first = convert_to_datetime(first)
            last = convert_to_datetime(last)
        except ValueError:
            return jsonify({'error': 'Unable to convert value to datetime.'}), 400
        return jsonify({ "days": get_days_between(first, last)}), 200
    return None


@app.route("/weekday", methods =["POST"])
def weekday() -> list:
    """Returns the day of the week a specific date is"""
    if request.method == "POST":
        add_to_history(request)
        if "date" not in request.json:
            return jsonify({"error": "Missing required data."}), 400
        data = request.json["date"]
        if not isinstance(data, str):
            return jsonify({'error': 'Unable to convert value to datetime.'}), 400
        try:
            first = convert_to_datetime(data)
        except ValueError:
            return jsonify({'error': 'Unable to convert value to datetime.'}), 400
        return jsonify({ "weekday": get_day_of_week_on(first)}), 200
    return None


@app.route("/history", methods =["GET", "DELETE"])
def history() -> dict:
    """Returns details on the last number of requests to the API"""
    global app_history
    add_to_history(request)
    if request.method == "GET":
        limit = 5
        if "number" in request.args:
            limit = request.args["number"]
            if not limit.isdigit():
                return jsonify({"error": "Number must be an integer between 1 and 20."}), 400
            limit = int(limit)
            if limit < 1 or limit > 20:
                return jsonify({"error": "Number must be an integer between 1 and 20."}), 400
        total = len(app_history)
        num = min([limit, total])
        return_arr =[]
        for i in range(total-1, total-num-1, -1):
            return_arr.append(app_history[i])
        return jsonify(return_arr), 200
    if request.method == "DELETE":
        app_history = []
        return jsonify({ "status": "History cleared" }), 200
    return None


if __name__ == "__main__":
    app.run(port=8080, debug=True)
