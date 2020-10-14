# models.py
import flask_sqlalchemy
from app import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<User: {}>".format(self.name)

class Texts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.now)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, text, user):
        self.text = text
        self.user = user
        
    def __repr__(self):
        return "<Text: {}\nBy: {}>\n".format(self.text, self.user)
