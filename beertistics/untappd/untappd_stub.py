import httplib2
from json import loads, load
import datetime
from beertistics import app
import flask
import os.path

def get_user_friends(username=None):
    if not username:
        username = 'valle'
    if not os.path.exists('stub/' + username):
        return False
    app.logger.info("Fetching user info for '%s' (stub)" % username)
    with open("stub/%s/user_friends.json" % username) as f:
        return load(f)

    return ["tnicolaysen", "valle"]

def get_user_info(username=None):
    if not username:
        username = 'valle'
    if not os.path.exists('stub/' + username):
        return False
    app.logger.info("Fetching user info for '%s' (stub)" % username)
    with open("stub/%s/user_info.json" % username) as f:
        return load(f)

def get_checkins(username=None):
    if not username:
        username = 'valle'
    if not os.path.exists('stub/' + username):
        return False
    app.logger.info("Fetching checkins for '%s' (stub)" % username)
    with open("stub/%s/checkins.json" % username) as f:
        return load(f)

def authenticate_url():
    return flask.url_for("authentication") + "?code=stub"

def authorize(code):
    if code == "stub":
        return "stub-token"
    else:
        return False

