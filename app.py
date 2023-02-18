""" This is a server application """
# pylint: disable=E1101
import os
from os.path import join, dirname
import flask
import flask_sqlalchemy
import flask_socketio
import requests
from dotenv import load_dotenv
import models


ADDRESSES_RECEIVED_CHANNEL = "messages received"
USER_COUNT = 0

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

with app.app_context():
    db.create_all()
    db.session.commit()


def chuck(data, jokebot_id):
    """ Requests a Chuck Norris joke through Rapid API and sends as message """
    db.session.add(models.Texts(data["message"], data["userId"]))
    url = "https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com/jokes/random"
    headers = {
        "x-rapidapi-host": "matchilling-chuck-norris-jokes-v1.p.rapidapi.com",
        "x-rapidapi-key": "17f5aa590cmshc9146e44a5c9835p18ab19jsn2ed7077f9dbc",
        "accept": "application/json",
    }
    response = requests.request("GET", url, headers=headers)
    joke = response.json()["value"]
    db.session.add(models.Texts(joke, jokebot_id))
    db.session.commit()
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)


def funtranslate(data, jokebot_id):
    """ Sends a request using requests.post to funtranslate API and receives json object """
    db.session.add(models.Texts(data["message"], data["userId"]))
    command = data["message"]
    message = command.split()
    message = " ".join(message[1:])
    response = requests.post(
        "https://api.funtranslations.com/translate/yoda.json", data={"text": message}
    )
    joke_msg = ""
    try:
        joke_msg = response.json()["contents"]["translated"]
    except:
        joke_msg = "We seem to have ran out of funtranslations requests"
        print("error with fun translate")
    db.session.add(models.Texts(joke_msg, jokebot_id))
    db.session.commit()
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)


def handle_command(data):
    """ receives messages that start with !! to be handled as commands """
    message = data["message"]
    jokebot = models.Users.query.filter_by(name="jokebot").first()
    if not jokebot:
        db.session.add(models.Users(name="jokebot", email="jokebot"))
        db.session.commit()
        jokebot = models.Users.query.filter_by(name="jokebot").first()
    command = message[2:]

    if command == "Chuck":
        chuck(data, jokebot.id)

    elif command.startswith("funtranslate"):
        funtranslate(data, jokebot.id)

    elif command == "about":
        joke_msg = "I'm jokebot. I'm here to help you have fun."
        db.session.add(models.Texts(joke_msg, jokebot.id))
        db.session.commit()
        emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)

    elif command == "help":
        joke_msg = "The commands I currently support are: !!Chuck, \
        !!funstranslate messageToBeTranslated, !!about, and !!clear"
        db.session.add(models.Texts(joke_msg, jokebot.id))
        db.session.commit()
        emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)

    elif command == "clear":
        try:
            db.session.query(models.Texts).delete()
            db.session.commit()
            emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
        except:
            return

    else:
        joke_msg = (
            "Beep boop I haven't been programmed to respond to that command beep boop."
        )
        db.session.add(models.Texts(joke_msg, jokebot.id))
        db.session.commit()
        emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)


def push_new_user_to_db(name, auth_type, email, auth_id, img_url=None):
    """ Checks if a user exists with the parameters given. If not, it creates it """
    user = models.Users.query.filter_by(name=name, email=email).first()
    if not user:
        if auth_type == models.AuthUserType.GOOGLE:
            db.session.add(models.Users(name, email, img_url, google_id=auth_id))
        else:
            db.session.add(models.Users(name, email, img_url, fb_id=auth_id))
        db.session.commit()
        return True
    return False


def emit_all_messages(channel):
    """ Emits messages to all the clients """
    all_messages = [
        {
            "message": db_texts.text,
            "userId": db_users.id,
            "username": db_users.name,
            "date": db_texts.date.strftime("%b %d, %I:%M %p"),
            "imgUrl": db_users.img_url if db_users.img_url else None,
        }
        for db_texts, db_users in db.session.query(models.Texts, models.Users)
        .filter(models.Texts.user == models.Users.id)
        .order_by(models.Texts.date)
        .all()
    ]
    socketio.emit(channel, {"allMessages": all_messages})


@socketio.on("connect")
def on_connect():
    """ sends socketId to client and message history """
    global USER_COUNT
    socketio.emit("count", {"count": USER_COUNT})
    curr_socket_id = flask.request.sid
    socketio.emit("connected", {"socketId": curr_socket_id}, room=curr_socket_id)
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)


@socketio.on("disconnect")
def on_disconnect():
    """ Reduces user count when a client disconnects and emits updated count """
    global USER_COUNT
    USER_COUNT -= 1
    socketio.emit("count", {"count": USER_COUNT})


@socketio.on("googleAuth")
def on_new_google_user(data):
    """ Handles the data received from a client-side google log in """
    global USER_COUNT
    USER_COUNT += 1
    socketio.emit("count", {"count": USER_COUNT})
    push_new_user_to_db(
        data["name"],
        models.AuthUserType.GOOGLE,
        data["email"],
        data["uid"],
        img_url=data["imgUrl"],
    )
    user = models.Users.query.filter_by(name=data["name"], email=data["email"]).first()
    socketio.emit(
        "send username",
        {"username": data["name"], "userId": user.id, "imgUrl": data["imgUrl"]},
        room=data["socketId"],
    )


@socketio.on("new msg")
def on_new_msg(data):
    """ Checks if messages are commands, adds user messages to db and sends to clients """
    message = data["message"]
    if message.startswith("!!"):
        handle_command(data)
    else:
        db.session.add(models.Texts(data["message"], data["userId"]))
        db.session.commit()
        emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)


@app.route("/")
def index():
    """ Renders html templates, emits messages to clients on connect """
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
