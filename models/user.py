import sqlite3
from db import db


class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # estas columnas deben coincidir con las propiedades de la clase, si no, no se guardan en db (pero
    # no fallan)

    def __init__(self, username, password):
        # No hace falta que pongas el id como propiedad, SQLAlchemy ya lo ha puesto por ti
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()