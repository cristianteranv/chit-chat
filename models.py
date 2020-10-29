''' These are sqlalchemy table declarations '''
# pylint: disable=E1101
from enum import Enum
from datetime import datetime
import flask_sqlalchemy
from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(100))
    google_id = db.Column(db.String())
    fb_id = db.Column(db.String())
    img_url = db.Column(db.String())
    def __init__(self, name, email, img_url=None, google_id=None, fb_id=None):
        self.name = name
        self.email = email
        if google_id:
            self.google_id = google_id
        if fb_id:
            self.fb_id = fb_id
        if img_url:
            self.img_url = img_url

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
