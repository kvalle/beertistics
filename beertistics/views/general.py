import flask
from flask import g
from json import dumps

from beertistics import app, auth, stats

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.render_template('index.html')
    else:
        return flask.render_template('login.html')

@app.route('/stats/basic')
@auth.requires_auth
def stats_basic():
    json = dumps(stats.basic(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})

