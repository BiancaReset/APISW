from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)

    def to_dict(self):
        return{
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_character = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    user_planet = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    user = db.relationship(User)

    def to_dict(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "user_character": self.user_character,
            "user_planet": self.user_planet
        }