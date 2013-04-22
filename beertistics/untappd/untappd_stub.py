import httplib2
from json import loads, load
import datetime
from beertistics import app, cache
import flask

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

@cache.cached("user_info")
def get_user_info(user=None):
    app.logger.info("Fetching user info for '%s' (stub)" % user)
    with open("data/user_info.json") as f:
        return load(f)

@cache.cached("checkins")
def get_checkins(user=None):
    app.logger.info("Fetching checkins for '%s' (stub)" % user)
    with open("data/checkins.json") as f:
        return load(f)

def authenticate_url():
    return flask.url_for("authentication") + "?code=stub"

def authorize(code):
    if code == "stub":
        return "stub-token"
    else:
        return False

