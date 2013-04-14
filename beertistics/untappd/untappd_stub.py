import httplib2
from json import loads, load
import datetime
from beertistics import app, cache
import flask

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def get_user_info(user=None):
    with open("data/user_info.json") as f:
        return load(f)

def get_checkins(user=None):
    with open("data/checkins.json") as f:
        return load(f)

def authenticate_url():
    return flask.url_for("authentication") + "?code=stub"

def authorize(code):
    if code == "stub":
        return "stub-token"
    else:
        return False

