from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120),nullable=False)
    height = db.Column(db.String(3), nullable=True)
    mass = db.Column(db.String(120),nullable=True)
    hair_color = db.Column(db.String(120), nullable=True)
    eye_color = db.Column(db.String(120), nullable=True)
    birth_year = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    created = db.Column(db.String(120), nullable=True)
    edited = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(120),  nullable=False)
    homeworld = db.Column(db.String(120), nullable=True)
    url = db.Column(db.String(120),nullable=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
        "id": self.id,
        "description": self.description,
        "height": self.height,
        "mass": self.mass,
        "hair_color": self.hair_color,
        "eye_color": self.eye_color,
        "birth_year": self.birth_year,
        "gender": self.gender,
        "created": self.created,
        "name": self.name,
        "homeworld": self.homeworld,
        "url": self.url,
    }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(3), nullable=False)
    orbital_period = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.String(120), nullable=False)
    created = db.Column(db.String(120), nullable=False)
    edited = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name  # Change "username" to an appropriate attribute

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created,
            "edited": self.edited,
            "name": self.name,
            "url": self.url,
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True) 
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True) 
    
    def __repr__(self):
        return '<Favorite %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }