# app.py
import requests
from os.path import join, dirname
from dotenv import load_dotenv
from flask import request
import json
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models
import re
import datetime


ADDRESSES_RECEIVED_CHANNEL = 'messages received'
user_count = 0

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.getenv('DATABASE_URL') 

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

def push_new_user_to_db(name, auth_type, email, authId, imgUrl=None):
    user = models.Users.query.filter_by(name=name, email=email).first()
    if not user:
        print("adding new user")
        if auth_type == models.AuthUserType.GOOGLE:
            db.session.add(models.Users(name, email, imgUrl, googleId = authId));
        else:
            db.session.add(models.Users(name, email, imgUrl, fbId = authId));
        db.session.commit();
        return True
#        emit_all_oauth_users(USERS_UPDATED_CHANNEL)
    else:
        print("user was already stored")
        #add new auth type if needed
        #if not user.googleId and auth_type == google:  db.UPDATE.SET(googleId=authId)
        return False

def emit_all_messages(channel):                                                                         #.strftime("%b %d, %I:%M %p")
    allMessages = [ \
        {'message': db_texts.text, 'userId' : db_users.id, 'username': db_users.name, 'date':db_texts.date.strftime("%b %d, %I:%M %p"), 'imgUrl': db_users.imgUrl if db_users.imgUrl else None}\
        for db_texts, db_users in \
        db.session.query(models.Texts,models.Users).filter(models.Texts.user == models.Users.id).order_by(models.Texts.date).all()\
        ]
#    print(allMessages[0]['date'])
    socketio.emit( channel, { 'allMessages': allMessages })

# db.session.query(Deliverable.column1, BatchInstance.column2).\
#     join(BatchInstance, Service, Supplier, SupplierUser). \
#     filter(SupplierUser.username == str(current_user)).\
#     order_by(Deliverable.created_time.desc()).all()
    
@socketio.on('connect')   #sends socketId to client and message history
def on_connect():
    global user_count
    socketio.emit('count', {'count': user_count})
    currSocketId = request.sid
    print('Someone connected with socketId: ', currSocketId)
    socketio.emit('connected', {
        'socketId': currSocketId
    }, room = currSocketId)
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():                #TODO HANDLE LOGOUT
    global user_count
    user_count -= 1
    socketio.emit('count', {'count': user_count})
    print ('Someone disconnected!')

@socketio.on('googleAuth')     #receives data from GoogleButton. Updates user count. Creates/Updates user row in db. 
def on_new_google_user(data):  #Sends username and userId to client.
    global user_count
    user_count += 1
    socketio.emit('count', {'count': user_count})
    print("Got an event for new google user input with data:", data)
    push_new_user_to_db(data['name'], models.AuthUserType.GOOGLE, data['email'], data['uid'], imgUrl=data['imgUrl'])
    user = models.Users.query.filter_by(name=data['name'], email=data['email']).first()
    socketio.emit('send username', {'username': data['name'], 'userId': user.id, 'imgUrl': data['imgUrl']}, room=data['socketId'])

@socketio.on('new msg')
def on_new_msg(data):
    print("Message \'{}\' received from: {} with userId: {}".format(data['message'], data['usrname'], data['userId']))
    #check the message for command
    message = data['message']
    if message.startswith("!!"):
        jokebot = models.Users.query.filter_by(name="jokebot").first()
        if not jokebot:
            db.session.add( models.Users(name = 'jokebot', email='jokebot'))
            db.session.commit()
            jokebot = models.Users.query.filter_by(name="jokebot").first()
        #about, help, funtranslate, unrecognized command, some command, some api
        command = message[2:]
        if command == "Chuck":
            db.session.add( models.Texts( data["message"], data['userId'] ) );
            #db.session.commit()
            url = "https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com/jokes/random"
            headers = {
                'x-rapidapi-host': "matchilling-chuck-norris-jokes-v1.p.rapidapi.com",
                'x-rapidapi-key': "17f5aa590cmshc9146e44a5c9835p18ab19jsn2ed7077f9dbc",
                'accept': "application/json"
            }
            response = requests.request("GET", url, headers=headers)
            joke = response.json()['value']
            print(joke, jokebot.id)
            db.session.add( models.Texts( joke, jokebot.id ) );
            db.session.commit()
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
        
        elif command.startswith("funtranslate"):
            db.session.add( models.Texts( data["message"], data['userId'] ) );
            message = command.split()
            message = " ".join(message[1:])
            url = "https://api.funtranslations.com/translate/yoda.json"
            response = requests.post('https://api.funtranslations.com/translate/yoda.json', data = {'text':message})
            jokeMsg = ""
            try:
                jokeMsg = response.json()['contents']['translated']
            except:
                jokeMsg = "We seem to have ran out of funtranslations requests"
                print("error with fun translate")
            db.session.add( models.Texts( jokeMsg, jokebot.id ) );
            db.session.commit()
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
            
        elif command == "about":
            jokeMsg = "I'm jokebot. I'm here to help you have fun."
            db.session.add( models.Texts( jokeMsg, jokebot.id ) );
            db.session.commit()
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
        
        elif command == "help":
            jokeMsg = "The commands I currently support are: !!Chuck, !!funstranslate messageToBeTranslated, !!about, and !!clear"
            db.session.add( models.Texts( jokeMsg, jokebot.id ) );
            db.session.commit()
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
        
        elif command == "clear":
            try:
                db.session.query(models.Texts).delete()
                db.session.commit()
                emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
            except:
                print("error when clearing texts table")
        
        else:
            jokeMsg = "Beep boop I haven't been programmed to respond to that command beep boop."
            db.session.add( models.Texts( jokeMsg, jokebot.id ) );
            db.session.commit()
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
        
    else:
        db.session.add( models.Texts( data['message'], data["userId"] ) );
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
