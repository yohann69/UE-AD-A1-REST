import json

# Ouverture du fichier JSON et chargement des données dans movies
with open('{}/databases/movies.json'.format("."), "r") as file:
    movies = json.load(file)

# Récupération d'un film par son id
def movie_with_id(_,info,_id):
    for movie in movies['movies']:
        if movie['id'] == _id:
            return movie
    raise ValueError("Movie with title [" + _id + "] not found.")

# Récupération d'un film par son titre
def movie_with_title(_, info, title):
    for movie in movies['movies']:
        if movie['title'] == title:
            return movie
    raise ValueError("Movie with title [" + title + "] not found.")

# Récupération de tous les films
def all_movies(_, info):
    return movies['movies']

# Modification de la note d'un film dans la base par son id
def update_movie_rating(_, info, _id, rating):
    for movie in movies['movies']:
        if movie['id'] == _id:
            movie['rating'] = rating
            return movie
    raise ValueError("Movie with id [" + _id + "] not found.")

# Ajout d'un film dans la base
def add_movie(_, info, title, director, rating):
    movie = {
        "id": len(movies['movies']) + 1,
        "director": director,
        "title": title,
        "rating": rating
    }
    movies['movies'].append(movie)
    with open('{}/databases/movies.json'.format("."), "w") as file:
        json.dump(movies, file)
    return movie
