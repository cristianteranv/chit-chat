# app.py
from os.path import join, dirname
from dotenv import load_dotenv
from flask import request
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models

ADDRESSES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

def emit_all_messages(channel):
    allMessages = [ \
        db_text.text for db_text in db.session.query(models.Texts).all()]
    print("all messages in emit all: ", allMessages)
    socketio.emit( channel, { 'allMessages': allMessages })
    print("Emitted")

@socketio.on('connect')
def on_connect():
    currSocketId = request.sid
    db.session.add( models.Users(currSocketId))
    db.session.commit()
    #use as name
    print('Someone connected with id: ', currSocketId)
    socketio.emit('connected', {
        'usrname': currSocketId #send user name
    }, room= currSocketId)
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new msg')
def on_new_msg(data):
    print("Server new msg received:", data)
    print("Message received from: ", data['usrname'])
    query = models.Users.query.filter_by(name=data['usrname']).first()
    db.session.add( models.Texts( data["message"], query.id ) );
    db.session.commit();
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
