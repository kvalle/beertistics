import flask
from flask import g
from json import dumps

from beertistics import app, auth, stats, cache

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.render_template('index.html')
    else:
        return flask.render_template('login.html')

@app.route('/photos')
def photos():
    return flask.render_template('photos.html')

@app.route('/stats/photos')
@auth.requires_auth
def stats_photos():
    json = dumps(stats.photos(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})

@app.route('/stats/basic')
@auth.requires_auth
def stats_basic():
    json = dumps(stats.basic(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})

@app.route('/stats/per-month')
@auth.requires_auth
def stats_per_month():
    json = dumps(stats.per_month(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})
