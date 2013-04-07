import flask
from json import dumps

from beertistics import app, auth, stats

def as_json_response(data):
    try:
        json = dumps(data, indent=4)
        return flask.Response(json, 200, {'content-type': 'text/plain'})
    except:
        err = "TODO: put an appropriate error message here. also, make sure 500s are handled correctly in client."
        return flask.Response(err, 500, {'content-type': 'text/plain'})

@app.route('/api/ratings')
@auth.requires_auth
def ratings():
    return as_json_response(stats.ratings())

@app.route('/api/photos')
@auth.requires_auth
def stats_photos():
    return as_json_response(stats.photos())

@app.route('/api/abv-vs-rating')
@auth.requires_auth
def abv_vs_rating():
    return as_json_response(stats.abv_vs_rating())

@app.route('/api/places')
@auth.requires_auth
def places():
    return as_json_response(stats.places())

@app.route('/api/basic')
@auth.requires_auth
def stats_basic():
    return as_json_response(stats.basic())

@app.route('/api/per-month')
@auth.requires_auth
def stats_per_month():
    return dumps(stats.per_month())
