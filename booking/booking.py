from flask import Flask, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound, Conflict

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

# Chargement du fichier JSON avec les réservations
with open('./databases/bookings.json', "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    """Page d'accueil du service Booking"""
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_all_bookings():
    """Retourne la base de données complète des réservations au format JSON"""
    return jsonify(bookings), 200


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    """Retourne les réservations d'un utilisateur en fonction de son ID"""
    user_bookings = [booking for booking in bookings if booking['userid'] == userid]
    if user_bookings:
        return jsonify(user_bookings), 200
    else:
        raise NotFound("No bookings found for the given user")


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_for_user(userid):
    """Ajoute une réservation pour un utilisateur spécifique"""
    new_booking = request.get_json()

    # Vérification de la validité du corps de la requête
    if "date" not in new_booking or "movieid" not in new_booking:
        return make_response(jsonify({"error": "Invalid input, missing 'date' or 'movieid'"}), 400)

    # Vérification des doublons (si une réservation existe déjà pour cette date et cet utilisateur)
    for booking in bookings:
        if booking['userid'] == userid:
            for date_item in booking['dates']:
                if date_item['date'] == new_booking['date'] and new_booking['movieid'] in date_item['movies']:
                    raise Conflict("Booking already exists for this user and movie on the given date")

    # Ajout de la réservation
    for booking in bookings:
        if booking['userid'] == userid:
            booking['dates'].append({
                "date": new_booking['date'],
                "movies": [new_booking['movieid']]
            })
            return make_response(jsonify({"message": "Booking added"}), 201)

    # Si l'utilisateur n'a pas encore de réservation, on en crée une nouvelle
    bookings.append({
        "userid": userid,
        "dates": [{
            "date": new_booking['date'],
            "movies": [new_booking['movieid']]
        }]
    })

    return make_response(jsonify({"message": "Booking added for new user"}), 201)


if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)
