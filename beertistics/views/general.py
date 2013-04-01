import flask
from flask import g

import beertistics.auth as auth
from beertistics import app

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.render_template('index.html')
    else:
        return flask.render_template('login.html')

@app.route('/settings')
@auth.requires_auth
def settings():
    return flask.render_template('settings.html')

@app.route('/json/profile')
@auth.requires_auth
def json_profile():
    json = "nothing yet"
    return flask.Response(json, 200, {'content-type': 'text/plain'})

