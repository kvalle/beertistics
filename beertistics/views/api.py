import flask
from json import dumps

from beertistics import app, auth, stats, untappd

def json_response(fn, *args):
    print app.logger.name
    try:
        data = fn(*args)
        json = dumps(data, indent=4)
        return flask.Response(json, 200, {'content-type': 'text/plain'})
    except Exception as e:
        msg = e.message if e.message and app.config["DEBUG"] else "An internal application fuckup occured. Sorry."
        return flask.Response(msg, 500, {'content-type': 'text/plain'})

@app.route('/api/beers-by-country')
@auth.requires_auth
def beers_by_country():
    return json_response(stats.beers_by_country)

@app.route('/api/map/checkins')
@auth.requires_auth
def map_checkins():
    return json_response(stats.map_checkins)

@app.route('/api/map/breweries')
@auth.requires_auth
def map_breweries():
    return json_response(stats.map_breweries)

@app.route('/api/rating-distribution')
@auth.requires_auth
def rating_distribution():
    return json_response(stats.rating_distribution)

@app.route('/api/photos')
@auth.requires_auth
def stats_photos():
    return json_response(stats.photos)

@app.route('/api/time-of-day')
@auth.requires_auth
def time_of_day():
    return json_response(stats.time_of_day)

@app.route('/api/rating-vs-abv')
@auth.requires_auth
def rating_vs_abv():
    return json_response(stats.rating_vs_abv)

@app.route('/api/checkin-locations')
@auth.requires_auth
def checkin_locations():
    return json_response(stats.checkin_locations)

@app.route('/api/basic')
@auth.requires_auth
def stats_basic():
    return json_response(stats.basic)

@app.route('/api/per-month')
@auth.requires_auth
def stats_per_month():
    return json_response(stats.per_month)
