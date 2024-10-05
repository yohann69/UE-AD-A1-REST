from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
    movies = json.load(jsf)["movies"]


def write(movies):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        dict = {}
        dict['movies'] = movies
        json.dump(dict, f)


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


@app.route("/movies/<movieId>", methods=['GET'])
def get_movie_byid(movieId):
    for movie in movies:
        if str(movie["id"]) == str(movieId):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "bad input parameter"}), 400)

@app.route("/movies/<movieId>", methods=['POST'])
def add_movie(movieId):
    req = request.get_json()
    for movie in movies:
        if str(movie["id"]) == str(movieId):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)
    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res

@app.route("/movies/<movieId>", methods=['DELETE'])
def del_movie(movieId):
    for movie in movies:
        if str(movie["id"]) == str(movieId):
            movies.remove(movie)
            return make_response("item deleted", 200)
    res = make_response(jsonify({"error": "ID not found"}), 400)
    return res


@app.route("/movies", methods=['GET'])
def get_movie_bytitle():
    title = request.args.get('title')
    for movie in movies:
        if movie["title"] == title:
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "movie title not found"}), 400)


@app.route("/movies/<movieId>/<rate>", methods=['PUT'])
def update_movie_rating(movieId, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieId):
            movie["rating"] = rate
            res = make_response("rate updated", 200)
            return res
    write(movies)
    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res



@app.route("/movies/<movieid>/description", methods=['GET'])
def get_movie_description(movieId):
    for movie in movies:
        if str(movie["id"]) == str(movieId):
            res = make_response(
                jsonify({"title": movie["title"], "rating": movie["rating"], "director": movie["director"]}), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


@app.route("/help", methods=['GET'])
def help():
    return make_response(jsonify({"GET /": "Welcome message",
                                    "GET /template": "HTML template",
                                    "GET /json": "Get all movies",
                                    "GET /movies/<movieId>": "Get movie by ID",
                                    "GET /movies?title=<title>": "Get movie by title",
                                    "GET /movies/<movieId>/description": "Get movie description",
                                    "POST /movies/<movieId>": "Add movie",
                                    "DELETE /movies/<movieId>": "Delete movie",
                                    "PUT /movies/<movieId>/<rate>": "Update movie rating"}),
                            200)


if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
