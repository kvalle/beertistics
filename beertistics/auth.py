import httplib2
from json import loads
from functools import wraps
import flask
from beertistics import app

def authorize(code):
    resp, content = httplib2.Http().request(authorize_url(code))
    json = loads(content)
    if json['meta']['http_code'] != 200:
        return False

    token = json['response']['access_token']
    flask.session['untappd_token'] = token
    flask.session['logged_in'] = True
    return True

def _build_url(base):
    return "http://untappd.com/oauth/" + base +"/" + \
        "?client_id=" + app.config['UNTAPPD_CLIENT_ID'] + \
        "&client_secret=" + app.config['UNTAPPD_CLIENT_SECRET'] + \
        "&redirect_url=" + flask.url_for('authentication', _external=True) + \
        "&response_type=code"

def authorize_url(code):    
    return _build_url('authorize') + "&code=" + code

def authenticate_url():
    return _build_url('authenticate')

def get_token():
    return flask.session.get('untappd_token', None)

def is_logged_in():
    return 'untappd_token' in flask.session

def logout():
    flask.session.pop('untappd_token', None)
    flask.session['logged_in'] = False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            flask.flash("You must log in to view this page.")
            flask.session['next_page'] = flask.request.url
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
