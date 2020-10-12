# models.py
import flask_sqlalchemy
from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Texts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now)
    user = db.Column(db.String(30), db.ForeignKey('user.id'))
    
    def __init__(self, text):
        self.text = text
        
    def __repr__(self):
        return "<Text: {}\nBy: {}".format(self.text, self.user)
