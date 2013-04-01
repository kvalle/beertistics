import flask
from flask import g

import beertistics.auth as auth
from beertistics import app

@app.route('/')
@auth.requires_auth
def index():
    return flask.render_template('index.html')


@app.route('/settings')
@auth.requires_auth
def index():
    return flask.render_template('settings.html')
