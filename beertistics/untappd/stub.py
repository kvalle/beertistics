import httplib2
from json import loads, load
import datetime
from beertistics import app
from beertistics.exceptions import NoSuchUserException
import flask
import os.path

def from_file(filename, username):
    if not username:
        username = 'valle'
    if not os.path.exists('stub/' + username):
        raise NoSuchUserException("There is no user with that username.")
    app.logger.info("Fetching %s for '%s' (stub)" % (filename, username))
    with open("stub/%s/%s" % (username, filename)) as f:
        return load(f)

def get_user_friends(username):
    return from_file("friend_list.json", username)

def get_user_info(username=None):
    return from_file("user_info.json", username)

def get_checkins(username):
    return from_file("checkin.json", username)

def authenticate_url():
    return flask.url_for("authentication") + "?code=stub"

def authorize(code):
    if code == "stub":
        return "stub-token"
    else:
        return False
