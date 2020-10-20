# models.py
import flask_sqlalchemy
from app import db
from datetime import datetime
from enum import Enum


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(100))
    googleId = db.Column(db.String())
    fbId = db.Column(db.String())
    imgUrl = db.Column(db.String())
    
    def __init__(self, name, email, googleId=None, fbId=None):
        self.name = name
        self.email = email
        if googleId:
            self.googleId = googleId
        if fbId:
            self.fbId = fbId
    
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
        
class AuthUserType(Enum):
    LINKEDIN = "linkedin"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    GITHUB = "github"
    PASSWORD = "password"
