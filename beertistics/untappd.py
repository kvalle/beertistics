import httplib2
from json import loads, load
import datetime
from beertistics import app, cache
import flask

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def url_params():
    return "client_id=" + app.config['UNTAPPD_CLIENT_ID'] + \
            "&client_secret=" + app.config['UNTAPPD_CLIENT_SECRET'] + \
            "&access_token=" + flask.session.get('untappd_token', None)

def get(url):
    print "FETCHING DATA FROM UNTAPPD:\n" + url
    _, content = httplib2.Http().request(url)
    return loads(content)

@cache.cached("user_info")
def get_user_info():
    return get("http://api.untappd.com/v4/user/info?" + url_params())

@cache.cached("checkins")
def get_checkins():
    json = get("http://api.untappd.com/v4/user/checkins?" + url_params())

    checkins = json["response"]["checkins"]["items"]
    next = json["response"]["pagination"]["next_url"]
    while next:
        next += url_params()
        print next
        json = get(next)
        checkins += json["response"]["checkins"]["items"]
        next = json["response"]["pagination"]["next_url"]

    return checkins

def get_checkins_stub():
    with open("beertistics/test.json") as f:
        return load(f)
