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

@app.route('/clear')
def clear_cache():
    return flask.redirect("/")

@app.route('/photos')
def photos():
    return flask.render_template('photos.html')

@app.route('/json/photos')
@auth.requires_auth
def stats_photos():
    json = dumps(stats.photos(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})

@app.route('/json/abv-vs-rating')
@auth.requires_auth
def abv_vs_rating():
    json = dumps(stats.abv_vs_rating(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})

@app.route('/json/places')
@auth.requires_auth
def places():
    json = dumps(stats.places(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})

@app.route('/json/basic')
@auth.requires_auth
def stats_basic():
    json = dumps(stats.basic(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})

@app.route('/json/per-month')
@auth.requires_auth
def stats_per_month():
    json = dumps(stats.per_month(), indent=4)
    return flask.Response(json, 200, {'content-type': 'text/plain'})
