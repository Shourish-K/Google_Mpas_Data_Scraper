from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    default_location = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    email_authenticated = db.Column(db.Boolean, default=False)
    search_history = db.relationship('SearchHistory')


class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String(100))
    geo_bias = db.Column(db.String(20))
    number_of_results = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    path = db.Column(db.String(1000), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
