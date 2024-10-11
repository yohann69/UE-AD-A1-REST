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

