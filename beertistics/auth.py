import unicodedata
import httplib2
from json import loads
from functools import wraps
import flask
from beertistics import app, untappd

def authorize(code):
    token = untappd.authorize(code)
    
    flask.session['untappd_token'] = token
    flask.session['logged_in'] = True
    flask.session['user'] = user_info()
    return True

def user_info():
    url = "http://api.untappd.com/v4/user/info?" + get_url_params()
    print "FETCHING " + url
    resp, content = httplib2.Http().request(url)
    json = loads(content)

    user = json['response']['user']
    return {
        'name': "%s %s" % (user['first_name'], user['last_name']),
        'username': user['user_name'],
        'avatar': user['user_avatar'],
        'url': user['untappd_url']
    }

def get_url_params():
    return "client_id=" + app.config['UNTAPPD_CLIENT_ID'] + \
            "&client_secret=" + app.config['UNTAPPD_CLIENT_SECRET'] + \
            "&access_token=" + flask.session.get('untappd_token', None)

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
