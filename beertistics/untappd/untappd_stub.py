import httplib2
from json import loads, load
import datetime
from beertistics import app
import flask
import os.path

def unknown_user():
    return {
        "meta": {
            "error_type": "invalid_auth", 
            "error_detail": "There is no user with that username.", 
            "code": 500, 
            "response_time": {"measure": "seconds", "time": 0.011}, 
            "developer_friendly": "" }, 
        "response": []
    }

def from_file(filename, username):
    if not username:
        username = 'valle'
    if not os.path.exists('stub/' + username):
        return unknown_user()
    app.logger.info("Fetching user info for '%s' (stub)" % username)
    with open("stub/%s/%s" % (username, filename)) as f:
        return load(f)

def get_user_friends(username=None):
    return from_file("user_friends.json", username)

def get_user_info(username=None):
    return from_file("user_info.json", username)

def get_checkins(username=None):
    return from_file("checkins.json", username)

def authenticate_url():
    return flask.url_for("authentication") + "?code=stub"

def authorize(code):
    if code == "stub":
        return "stub-token"
    else:
        return False

