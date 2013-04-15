import flask
from json import dumps

from beertistics import app, auth, stats, untappd

def as_json_response(data):
    try:
        json = dumps(data, indent=4)
        return flask.Response(json, 200, {'content-type': 'text/plain'})
    except TypeError as e:
        print e
        err = "TODO: put an appropriate error message here. also, make sure 500s are handled correctly in client."
        return flask.Response(err, 500, {'content-type': 'text/plain'})

@app.route('/api/test/<string:user>')
@auth.requires_auth
def api_test(user):
    return as_json_response(untappd.get_user_info(user))

@app.route('/api/beers-by-country')
@auth.requires_auth
def beers_by_country():
    return as_json_response(stats.beers_by_country())

@app.route('/api/map/checkins')
@auth.requires_auth
def map_checkins():
    return as_json_response(stats.map_checkins())

@app.route('/api/map/breweries')
@auth.requires_auth
def map_breweries():
    return as_json_response(stats.map_breweries())

@app.route('/api/rating-distribution')
@auth.requires_auth
def rating_distribution():
    return as_json_response(stats.rating_distribution())

@app.route('/api/photos')
@auth.requires_auth
def stats_photos():
    return as_json_response(stats.photos())

@app.route('/api/time-of-day')
@auth.requires_auth
def time_of_day():
    return as_json_response(stats.time_of_day())

@app.route('/api/rating-vs-abv')
@auth.requires_auth
def rating_vs_abv():
    return as_json_response(stats.rating_vs_abv())

@app.route('/api/checkin-locations')
@auth.requires_auth
def checkin_locations():
    return as_json_response(stats.checkin_locations())

@app.route('/api/basic')
@auth.requires_auth
def stats_basic():
    return as_json_response(stats.basic())

@app.route('/api/per-month')
@auth.requires_auth
def stats_per_month():
    return dumps(stats.per_month())
