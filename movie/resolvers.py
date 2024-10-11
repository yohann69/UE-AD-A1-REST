import json

def movie_with_id(_,info,_id):
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

