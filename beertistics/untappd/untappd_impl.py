import httplib2
from json import loads, load
import datetime
from beertistics import app
import flask

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

##
## Public functions
##

def get_user_info(user=None):
    url = "http://api.untappd.com/v4/user/info"
    if user:
        url += "/%s" % user
    url += "?%s" % _url_params()
    return _get(url)

def get_checkins(user=None):
    url = "http://api.untappd.com/v4/user/checkins"
    if user:
        url += "/%s" % user
    url += "?%s" % _url_params()
    url += "&limit=100"
    json = _get(url)

    checkins = json["response"]["checkins"]["items"]
    next = json["response"]["pagination"]["next_url"]
    while next:
        next += "&" + _url_params()
        next += "&limit=100"
        print next
        json = _get(next)
        checkins += json["response"]["checkins"]["items"]
        next = json["response"]["pagination"]["next_url"]

    return checkins

def authenticate_url():
    url = _build_url('authenticate')
    print url
    return url

def authorize(code):
    url = _build_url('authorize') + "&code=" + code
    resp, content = httplib2.Http().request(url)
    json = loads(content)

    if json['meta']['http_code'] != 200:
        return False

    return json['response']['access_token']

##
## Helper functions for making calls to Untappd
##

def _url_params():
    return "client_id=" + app.config['UNTAPPD_CLIENT_ID'] + \
            "&client_secret=" + app.config['UNTAPPD_CLIENT_SECRET'] + \
            "&access_token=" + flask.session.get('untappd_token', None)

def _get(url):
    print "FETCHING DATA FROM UNTAPPD:\n" + url
    _, content = httplib2.Http().request(url)
    return loads(content)

def _build_url(base):
    return "http://untappd.com/oauth/" + base +"/" + \
        "?client_id=" + app.config['UNTAPPD_CLIENT_ID'] + \
        "&client_secret=" + app.config['UNTAPPD_CLIENT_SECRET'] + \
        "&redirect_url=" + flask.url_for('authentication', _external=True) + \
        "&response_type=code"
