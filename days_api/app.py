"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, Response, request, jsonify

from date_functions import convert_to_datetime, get_day_of_week_on, get_days_between



app = Flask(__name__)
app_history = []
print(app_history )

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
    add_to_history(request)
    return jsonify({ "message": "Welcome to the Days API." })


@app.route("/between", methods =["POST"])
def get_between():
    """Returns the number of days between two dates"""
    add_to_history(request)
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
    add_to_history(request)
    try:
        first = convert_to_datetime(request.json["date"])
    except:
        return jsonify({'error': True,
                        'message': 'Could not convert to datetime, check format.'}), 400
    return jsonify({ "weekday": get_day_of_week_on(first)}), 200


@app.route("/history", methods =["GET", "DELETE"])
def get_or_delete_history():
    """Returns details on the last number of requests to the API"""
    global app_history
    add_to_history(request)
    if request.method == "GET":
        limit = 5
        if "number" in request.args:
            limit = request.args["number"]
            if not limit.isdigit():
                return jsonify({'error': True,
                            'message': 'number is not an integer'}), 400
            limit = int(limit)
            if limit < 1 or limit > 20:
                return jsonify({'error': True,
                            'message': 'number must be between 1 and 20'}), 400
        num = min([limit, len(app_history)])
        return_arr =[]
        for i in range(num):
            return_arr.append(app_history[i])
        return jsonify(return_arr), 200
    if request.method == "DELETE":
        app_history = []
        return jsonify({ "status": "History cleared" }), 200


if __name__ == "__main__":
    app.run(port=8080, debug=True)
