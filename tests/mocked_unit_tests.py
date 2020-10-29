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
from app import push_new_user_to_db, emit_all_messages, funtranslate, handle_command

KEY_INPUT="input"
KEY_EXPECTED="expected"
KEY_NAME="name"
KEY_AUTH_TYPE="auth type"
KEY_EMAIL="email"
KEY_AUTH_ID="auth id"


class mockJSON:
    def __init__(self, dic):
        self.dic = dic
        
    def json(self):
        return self.dic


class chuck_testcase(unittest.TestCase):
    def mock_models_Texts(self, message, userId):
        if message == None or userId == None:
            raise ValueError("message or userId are None")
    
    def mock_session_add(self, modelsTexts):
        return None
    
    def mock_session_commit(self):
        return None
    
    def mock_requests_request(self, get, url, headers):
        return mockJSON({"value": "this is a chuck norris joke"})

    def mock_emit_all_messages(self, channel):
        return None
    
    
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: ""
            },
        ]
        
    def test_chuck_testcase_success(self):
        with mock.patch("app.emit_all_messages", self.mock_emit_all_messages), mock.patch("requests.request", self.mock_requests_request), \
        mock.patch("sqlalchemy.orm.scoping.scoped_session.add", self.mock_session_add), mock.patch("sqlalchemy.orm.scoping.scoped_session.commit", self.mock_session_commit):
            for testcase in self.success_test_params:
                app.chuck({"message": "text message", "userId": 2}, 1)

class funtranslate_testcase(unittest.TestCase):
    def mock_session_add(self, modelsTexts):
        return None
        
    def mock_session_commit(self):
        return None
        
    def mock_models_Texts(self, message, userId):
        if message == None or userId == None:
            raise ValueError("message or userId are None")
        
    def mock_emit_all_messages(self, channel):
        return None
        
    def mock_requests_post(self, url, data):
        if data:
            return mockJSON({"contents": {"translated": "yoda, this is."}})
        else:
            return None
    
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message":"this is yoda.", "userId": 2},
                KEY_EXPECTED: ""
            },
        ]
        
    def test_funtranslate_testcase_success(self): #check if message is empty
        with mock.patch("app.emit_all_messages", self.mock_emit_all_messages), mock.patch("requests.post", self.mock_requests_post), \
        mock.patch("sqlalchemy.orm.scoping.scoped_session.add", self.mock_session_add), mock.patch("sqlalchemy.orm.scoping.scoped_session.commit", self.mock_session_commit):
            for testcase in self.success_test_params:
                app.funtranslate(testcase[KEY_INPUT], 1)
                
class handle_command_testcase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {"message": "!!Chuck", "userId": 1},
                KEY_EXPECTED: ""
            },
            {
                KEY_INPUT: {"message": "!!funtranslate this is yoda"},
                KEY_EXPECTED: ""
            },
            {
                KEY_INPUT: {"message": "!!about"},
                KEY_EXPECTED: ""
            },
            {
                KEY_INPUT: {"message": "!!help"},
                KEY_EXPECTED: ""
            },
            {
                KEY_INPUT: {"message": "!!clear"},
                KEY_EXPECTED: ""
            },
            {
                KEY_INPUT: {"message": "!!SomethingElse"},
                KEY_EXPECTED: ""
            },
        ]
        
    def mock_session_add(self, modelsTexts):
        return None

    def mock_session_commit(self):
        return None

    def mock_models_Texts(self, message, userId):
        if message == None or userId == None:
            raise ValueError("message or userId are None")

    def mock_emit_all_messages(self, channel):
        return None

    def mock_chuck(self, data, jokebotId):
        return None

    def mock_funtranslate(self, data, jokebotId):
        return None

    def test_handle_command_testcase_success(self):
        with mock.patch("app.emit_all_messages", self.mock_emit_all_messages), mock.patch("models.Texts", self.mock_models_Texts), \
        mock.patch("sqlalchemy.orm.scoping.scoped_session.add", self.mock_session_add), mock.patch("sqlalchemy.orm.scoping.scoped_session.commit", self.mock_session_commit),\
        mock.patch("app.chuck", self.mock_chuck), mock.patch("app.funtranslate", self.mock_funtranslate):
            for testcase in self.success_test_params:
                handle_command(testcase[KEY_INPUT])

class push_new_user_to_db_testcase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_NAME: "UnstoredName",
                KEY_AUTH_TYPE: AuthUserType.GOOGLE,
                KEY_EMAIL: "email@gmail.com",
                KEY_AUTH_ID: "ABCD1234"
            },
            {
                KEY_NAME: "UnstoredName",
                KEY_AUTH_TYPE: AuthUserType.FACEBOOK,
                KEY_EMAIL: "email@gmail.com",
                KEY_AUTH_ID: "ABCD1234"
            },
            {
                KEY_NAME: "jokebot",
                KEY_AUTH_TYPE: AuthUserType.GOOGLE,
                KEY_EMAIL: "jokebot",
                KEY_AUTH_ID: "ABCD1234"
            },
        ]

    def mock_session_commit(self):
        return None

    def mock_models_Users(self, name, email, imgUrl):
        return None
    
    def mock_session_add(self, modelsUsers):
        return None
        
    def test_push_new_user_to_db_success(self):
        with mock.patch("sqlalchemy.orm.scoping.scoped_session.add", self.mock_session_add), \
        mock.patch("sqlalchemy.orm.scoping.scoped_session.commit", self.mock_session_commit):
            for testcase in self.success_test_params:
                push_new_user_to_db(testcase[KEY_NAME], testcase[KEY_AUTH_TYPE], testcase[KEY_EMAIL], testcase[KEY_AUTH_ID])

class on_new_msg(unittest.TestCase):
    def setUp(self):
        self.test_params = [
            {
                "message": "!!command",
                "userId": 1
            },
            {
                "message": "not a command",
                "userId": 2
            }
        ]

    def mock_session_commit(self):
        return None

    def test_on_new_msg(self):
        with mock.patch("sqlalchemy.orm.scoping.scoped_session.commit", self.mock_session_commit):
            for testcase in self.test_params:
                app.on_new_msg(testcase)

if __name__ == '__main__':
    unittest.main()