from functools import wraps
import flask
from beertistics import untappd

def authorize(code):
    token = untappd.authorize(code)
    
    flask.session['untappd_token'] = token
    flask.session['logged_in'] = True
    flask.session['user'] = untappd.logged_in_user_info()
    return True

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
            flask.session['next_page'] = flask.request.url
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
