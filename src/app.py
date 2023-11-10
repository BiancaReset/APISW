"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite 

app = Flask(__name__)

app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
MIGRATE = Migrate(app, db)
db.init_app(app)


CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')

def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET', "POST"])
def handle_user():
    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.to_dict(), users))

        return jsonify({
            "data": users
        }), 200
    
    elif request.method == 'POST':
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({
                "error": "Invalid content type. Use application/json."
            }), 400

        user = User()
        data = request.get_json()
        user.email = data["email"]
        user.password = data["password"]

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "msg": "Usuario creado"
        }), 200


@app.route("/user/<int:id>", methods=["GET","PUT", "DELETE"])
def update_user(id):
    if request.method == 'GET':
        user_id = id
        user = User.query.get(id)
        data = user.to_dict()

        return data, 200
    elif request.method == 'PUT':
        user = User.query.get(id)
        if user is not None:
            data = request.get_json()
            user.name = data["name"]
            user.email = data["email"]
            db.session.commit()
            return jsonify({
                "msg":"Usuario actualizado"
            }),200
        else:
            return jsonify({
                "msg": "Usuario no encontrado"
            }), 404
    elif request.method == 'DELETE':
        user = User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()

            return jsonify({
                "msg":"Usuario eliminado"
            }),202
        else:
            return jsonify({
                "msg":"Usuario no encontrado"
            }), 404

@app.route('/character', methods=['GET', "POST"])
def handle_character():
    if request.method == 'GET':
        characters = Character.query.all()
        characters = list(map(lambda character: character.to_dict(), characters))

        return jsonify({
            "data": characters
        }), 200
    elif request.method == 'POST':
        character = Character()
        data = request.get_json()
        character.name = data["name"]

        db.session.add(character)
        db.session.commit()

        return jsonify({
            "msg": "Personaje creado"
        }), 200

@app.route("/character/<int:id>", methods=["PUT", "DELETE"])
def update_character(id):
    if request.method == 'PUT':
        character = Character.query.get(id)
        if character is not None:
            data = request.get_json()
            character.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"Personaje actualizado"
            }),200
        else:
            return jsonify({
                "msg": "Personaje no encotrado"
            }), 404
    elif request.method == 'DELETE':
        character = Character.query.get(id)
        if character is not None:
            db.session.delete(character)
            db.session.commit()

            return jsonify({
                "msg":"Personaje eliminado"
            }),202
        else:
            return jsonify({
                "msg":"Personaje no encontrado"
            }), 404

@app.route('/planet', methods=['GET', "POST"])
def handle_planet():
    if request.method == 'GET':
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.to_dict(), planets))

        return jsonify({
            "data": planets
        }), 200
    elif request.method == 'POST':
        planet = Planet()
        data = request.get_json()
        planet.name = data["name"]

        db.session.add(planet)
        db.session.commit()

        return jsonify({
            "msg": "Planeta creado"
        }), 200

@app.route("/planet/<int:id>", methods=["PUT", "DELETE"])
def update_planet(id):
    if request.method == 'PUT':
        planet = Planet.query.get(id)
        if planet is not None:
            data = request.get_json()
            planet.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"Planeta actualizado"
            }),200
        else:
            return jsonify({
                "msg": "Planeta no encontrado"
            }), 404
    elif request.method == 'DELETE':
        planet = Planet.query.get(id)
        if planet is not None:
            db.session.delete(planet)
            db.session.commit()

            return jsonify({
                "msg":"Planeta eliminado"
            }),202
        else:
            return jsonify({
                "msg":"Planeta no encontrado"
            }), 404

@app.route('/user/<int:id>/favorite', methods=['GET'])
def handle_favorite(id):
    user_id = id
    favorites = Favorite.query.filter_by(user_id=user_id)
    favorites = list(map(lambda favorite: favorite.to_dict(), favorites))

    return jsonify({
        "data": favorites
    }), 200
    
@app.route('/favorite', methods=["POST"])
def create_favorite():
    favorite = Favorite()
    data = request.get_json()
    user_id = data["user_id"]
    if data["character_id"] is None:
        character_id = "0"
    character_id = data["character_id"]
    if data["planet_id"] is None:
        planet_id = "0"
    planet_id = data["planet_id"]
    

    user_filter = User.query.filter_by(id=user_id)
    character_filter = Character.query.filter_by(id=character_id)
    planet_filter = Planet.query.filter_by(id=planet_id)

    if user_filter is not None and character_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_character = data["character_id"]
        favorite.planet_id = data["planet_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "Favorito creado"
        }), 200

    elif user_filter is not None and planet_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_planet = data["planet_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "Favorito creado"
        }), 200

    else:
        return jsonify({
                "msg":"No se pudo crear el favorito. Asegúrate que el usuario, personaje o planeta existan"
            }), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)