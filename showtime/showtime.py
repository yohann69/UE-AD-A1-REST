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


@app.route("/json", methods=['GET'])
def get_schedule():
    """Get the full JSON database of showtimes"""
    return jsonify(schedule)


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie(movieid):
    """Get movie details by its ID"""
    try:
        # Return the movie data for the given movie ID
        return jsonify(schedule[movieid])
    except KeyError:
        # Raise a 404 error if the movie ID is not found
        raise NotFound("Movie not found")


@app.route("/addmovie", methods=['POST'])
def add_movie():
    """Add a new movie to the schedule"""
    movie = request.get_json()
    # Add the movie to the schedule using the movie's ID
    schedule[movie["id"]] = movie
    return make_response(jsonify({"message": "Movie added"}), 201)


if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)
