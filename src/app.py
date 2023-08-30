"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, People, Planet
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this "super secret" with something else!
jwt = JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user_id": user.id})

@app.route('/people', methods=['GET'])
@jwt_required()
def get_all_people():
    people_list = People.query.all()
    serialized_people = [person.serialize() for person in people_list]
    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
@jwt_required()
def get_single_person(people_id):
    person = People.query.get(people_id)
    if person is not None:
        serialized_person = person.serialize()
        return jsonify(serialized_person), 200
    else:
        return jsonify({"message": "Person not found"}), 404
    
@app.route('/planets', methods=['GET'])
@jwt_required()
def get_all_planets():
    planets_list = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets_list]
    return jsonify(serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
@jwt_required()
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is not None:
        serialized_planet = planet.serialize()
        return jsonify(serialized_planet), 200
    else:
        return jsonify({"message": "Planet not found"}), 404    

@app.route('/users', methods=['GET'])
@jwt_required()
def get_user():
    results = []
    users = User.query.all()
    for user in users:
        results.append(user.serialize())
    return jsonify (results), 200

@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_user_favorite():
    current_user_id = get_jwt_identity()  
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    
    favorite_list = []
    for favorite in favorites:
        favorite_list.append(favorite.serialize())
    
    return jsonify(favorite_list), 200

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
@jwt_required()
def add_favorite_planet(planet_id):
    current_user_id = get_jwt_identity()  
    new_favorite = Favorite(
        user_id=current_user_id,
        planet_id=planet_id,
    )
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet added successfully"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
@jwt_required()
def add_favorite_people(people_id):
    current_user_id = get_jwt_identity()  
    new_favorite = Favorite(
        user_id=current_user_id,
        character_id=people_id,
    )
    
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite people added successfully"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_planet(planet_id):
    current_user_id = get_jwt_identity()  
    favorite_to_delete = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if favorite_to_delete:
        db.session.delete(favorite_to_delete)
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted successfully"}), 200
    else:
        return jsonify({"message": "Favorite planet not found"}), 404
    
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_people(people_id):
    current_user_id = get_jwt_identity()  
    favorite_to_delete = Favorite.query.filter_by(user_id=current_user_id, character_id=people_id).first()
    
    if favorite_to_delete:
        db.session.delete(favorite_to_delete)
        db.session.commit()
        return jsonify({"message": "Favorite person deleted successfully"}), 200
    else:
        return jsonify({"message": "Favorite person not found"}), 404


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)