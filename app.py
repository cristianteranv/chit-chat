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

ADDRESSES_RECEIVED_CHANNEL = 'messages received'
user_count = 0

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

# sql_user = os.environ['SQL_USER']
# sql_pwd = os.environ['SQL_PASSWORD']
# dbuser = os.environ['USER']

database_uri = os.getenv('DATABASE_URL') 

#'postgresql://{}:{}@localhost/postgres'.format(sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()


def emit_all_messages(channel):
    allMessages = [ \
        {'message': db_texts.text, 'usrname' : db_users.name}\
        for db_texts, db_users in \
        db.session.query(models.Texts,models.Users).filter(models.Texts.user == models.Users.id).order_by(models.Texts.date).all()\
        ]
    
    socketio.emit( channel, { 'allMessages': allMessages })
    print("Emitted")

# db.session.query(Deliverable.column1, BatchInstance.column2).\
#     join(BatchInstance, Service, Supplier, SupplierUser). \
#     filter(SupplierUser.username == str(current_user)).\
#     order_by(Deliverable.created_time.desc()).all()
    
@socketio.on('connect')
def on_connect():
    global user_count
    user_count += 1
    currSocketId = request.sid
    db.session.add( models.Users(currSocketId))
    db.session.commit()
    print('Someone connected with id: ', currSocketId)
    socketio.emit('connected', {
        'usrname': currSocketId
    }, room = currSocketId)
    
    socketio.emit('count', {'count': user_count})
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    global user_count
    user_count -= 1
    socketio.emit('count', {'count': user_count})
    print ('Someone disconnected!')

@socketio.on('new msg')
def on_new_msg(data):
    print("Server new msg received:", data)
    print("Message received from: ", data['usrname'])
    #check the message for command
    message = data['message']
    if message.startswith("!!"):
        jokebot = models.Users.query.filter_by(name="jokebot").first()
        #about, help, funtranslate, unrecognized command, some command, some api
        print("Received a bot command")
        command = message[2:]
        if command == "Chuck":
            userquery = models.Users.query.filter_by(name=data['usrname']).first()
            db.session.add( models.Texts( data["message"], userquery.id ) );
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
            print("here")
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
        
        elif command.startswith("funtranslate"):
            userquery = models.Users.query.filter_by(name=data['usrname']).first()
            db.session.add( models.Texts( data["message"], userquery.id ) );
            message = command.split()
            message = " ".join(message[1:])
            print("message to fun translate: {}".format(message))
            url = "https://api.funtranslations.com/translate/yoda.json"
            response = requests.post('https://api.funtranslations.com/translate/yoda.json', data = {'text':message})
            jokeMsg = ""
            try:
                print("Funtranslate response: ", response)
                jokeMsg = response.json()['contents']['translated']
                print("Translated text: ", jokeMsg)
            except:
                jokeMsg = "We seem to have ran out of funtranslations requests"
                print("error")
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
                print("error")
        
        else:
            jokeMsg = "Beep boop I haven't been programmed to respond to that command beep boop."
            db.session.add( models.Texts( jokeMsg, jokebot.id ) );
            db.session.commit()
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
        
    else:  
        userquery = models.Users.query.filter_by(name=data['usrname']).first()
        db.session.add( models.Texts( data["message"], userquery.id ) );
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
