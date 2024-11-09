from . import db # from website import db (If importing outside of directory)
from flask_login import UserMixin # Used to create sessions
from sqlalchemy import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Defines the column in the database
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100)) # removed , unique=True
    password = db.Column(db.String(1000))