import unittest
import unittest.mock as mock
from dotenv import load_dotenv
import os
import datetime
from models import AuthUserType
from os.path import join, dirname
import sys
sys.path.append(join(dirname(__file__), "../"))
import app
from app import push_new_user_to_db, emit_all_messages, funtranslate

KEY_INPUT="input"
KEY_EXPECTED="expected"
KEY_NAME="name"
KEY_AUTH_TYPE="auth type"
KEY_EMAIL="email"
KEY_AUTH_ID="auth id"

class emit_all_messages(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: ""
            },
        ]
        
    def test_emit_all_messages_testcase_success(self):
        for testcase in self.success_test_params:
            app.emit_all_messages("messages received")

class on_new_google_user(unittest.TestCase): #unmocked
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: ""
            }
        ]

    def test_on_new_google_user(self):
        for testcase in self.success_test_params:
            app.on_new_google_user({"name": "jokebot", "email": "jokebot", "uid": "", "imgUrl": "", "socketId": "whatever"})
            
class on_disconnect(unittest.TestCase): #unmocked
    def test_on_disconnect(self):
        app.on_disconnect()
        
class on_connect(unittest.TestCase):
    @mock.patch('app.flask')
    def test_on_connect(self, mock_flask):
        mock_flask.request.sid = "mock_sid"
        app.on_connect()