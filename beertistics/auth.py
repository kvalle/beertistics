import hashlib
from functools import wraps
import flask
from flask import g
from beertistics import app

def login(username, password):
    if not _check(username, password): 
        return False
    flask.session['logged_in'] = True
    return True

def logout():
    flask.session.pop('logged_in', None)

def _check(username, password):
    if not username == app.config['USERNAME']:
        return False
    return app.config['PASSWORD'] == hashlib.sha1(password).hexdigest()

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not flask.session.get('logged_in', False):
            flask.flash("You must log in to view this page.")
            flask.session['next_page'] = flask.request.url
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
