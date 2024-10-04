from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

# Load the schedule from the JSON file
with open('./databases/times.json', "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=['GET'])
def get_schedule():
    """Get the full JSON schedule database"""
    return jsonify({"schedule": schedule})


@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    """Get the schedule by date"""
    result = [entry for entry in schedule if entry["date"] == date]
    if result:
        return jsonify(result[0])
    else:
        return make_response(jsonify({"error": "Bad input parameter"}), 400)


if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)
