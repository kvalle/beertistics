import flask
from flask import g

import beertistics.auth as auth
from beertistics import app
from beertistics import untappd_wrapper as untappd

@app.route('/')
def index():
    return flask.render_template('index.html', token=auth.get_token())

@app.route('/settings')
@auth.requires_auth
def settings():
    return flask.render_template('settings.html')

@app.route('/json/profile')
@auth.requires_auth
def json_profile():
    json = untappd.user_info()
    return flask.Response(json, 200, {'content-type': 'text/plain'})

