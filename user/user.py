from crypt import methods

from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

# URl of the services
BOOKING_SERVICE_URL = "http://localhost:3201"
MOVIES_SERVICE_URL = "http://localhost:3200"
SHOWTIMES_SERVICE_URL = "http://localhost:3202"

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/user/<userId>/bookings", methods=['GET'])
def get_booking_for_user(userId):

   # Check if the user exists
   for user in users:
      if user["id"] == userId:

         # Get the bookings for the user
         bookingsObject = requests.get(BOOKING_SERVICE_URL + "/bookings/" + userId)

         if bookingsObject.status_code == 200:

            # Return the bookings
            return bookingsObject.json()
         else:

            # Return an error if the booking is not found
            return bookingsObject

      return make_response(jsonify({"error": "ID not found"}), 201)

@app.route("/user/<userId>/bookings/movies", methods=["GET"])
def get_movies_from_user_bookings(userId):

    # Check if the user exists
   for user in users:
      if user["id"] == userId:

         # Get the bookings for the user
         userBookings = get_booking_for_user(userId)
         if len(userBookings) > 0:
            userBookings = get_booking_for_user(userId)[0]

            # Get the movies for the bookings
            for i in range(len(userBookings["dates"])):
               for y in range(len(userBookings["dates"][i]["movies"])):

                  # Get the movie information
                  movieInformation = requests.get(
                     MOVIES_SERVICE_URL + "/movies/" + userBookings["dates"][i]["movies"][y])

                  # Add the movie information to the booking
                  # If the movie is found and if is not found an error information
                  if movieInformation.status_code == 200:
                     userBookings["dates"][i]["movies"][y] = movieInformation.json()
                  else:
                     userBookings["dates"][i]["movies"][y] = jsonify({"error": "movie not found"})

            # Return the movies
            return userBookings

   return make_response(jsonify({"error": "ID not found"}), 201)



if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
