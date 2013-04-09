import flask
from json import dumps

from beertistics import app, auth, stats

def as_json_response(data):
    try:
        json = dumps(data, indent=4)
        return flask.Response(json, 200, {'content-type': 'text/plain'})
    except TypeError as e:
        print e
        err = "TODO: put an appropriate error message here. also, make sure 500s are handled correctly in client."
        return flask.Response(err, 500, {'content-type': 'text/plain'})

@app.route('/api/test')
@auth.requires_auth
def api_test():
    return as_json_response(stats.test())

@app.route('/api/map/checkins')
@auth.requires_auth
def map_checkins():
    return as_json_response(stats.map_checkins())

@app.route('/api/map/breweries')
@auth.requires_auth
def map_breweries():
    return as_json_response(stats.map_breweries())

@app.route('/api/ratings')
@auth.requires_auth
def ratings():
    return as_json_response(stats.ratings())

@app.route('/api/photos')
@auth.requires_auth
def stats_photos():
    return as_json_response(stats.photos())

@app.route('/api/time-of-day')
@auth.requires_auth
def time_of_day():
    return as_json_response(stats.time_of_day())

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
