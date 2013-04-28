import flask
import traceback
from functools import wraps
from json import dumps

from beertistics import app, auth, stats, untappd, user_service

def json_response(fn, *args):
    try:
        data = fn(*args)
        json = dumps(data, indent=4)
        return flask.Response(json, 200, {'content-type': 'text/plain'})
    except Exception as e:
        stacktrace = traceback.format_exc()
        app.logger.error('problem fetching json-data: %s\n%s', e.message, stacktrace)
        msg = e.message if e.message and app.config["DEBUG"] else "An internal application fuckup occured. Sorry."
        return flask.Response(msg, 500, {'content-type': 'text/plain'})

def fail_unless_logged_in(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not auth.is_logged_in():
            return flask.Response("User not logged in.", 500, {'content-type': 'text/plain'})
        return f(*args, **kwargs)
    return decorated

@app.route('/api/test')
@fail_unless_logged_in
def test():
    return json_response(stats.test)

@app.route('/api/friends/')
@fail_unless_logged_in
def friends():
    return json_response(user_service.user_friends)

@app.route('/api/influenced-ratings')
@fail_unless_logged_in
def influenced_ratings():
    return json_response(stats.influenced_ratings)

@app.route('/api/beers-by-country-as-list')
@fail_unless_logged_in
def beers_by_country_as_list():
    return json_response(stats.beers_by_country_as_list)

@app.route('/api/beers-by-country')
@fail_unless_logged_in
def beers_by_country():
    return json_response(stats.beers_by_country)

@app.route('/api/map/checkins')
@fail_unless_logged_in
def map_checkins():
    return json_response(stats.map_checkins)

@app.route('/api/map/breweries')
@fail_unless_logged_in
def map_breweries():
    return json_response(stats.map_breweries)

@app.route('/api/rating-distribution')
@fail_unless_logged_in
def rating_distribution():
    return json_response(stats.rating_distribution)

@app.route('/api/photos')
@fail_unless_logged_in
def stats_photos():
    return json_response(stats.photos)

@app.route('/api/time-of-day')
@fail_unless_logged_in
def time_of_day():
    return json_response(stats.time_of_day)

@app.route('/api/rating-vs-abv')
@fail_unless_logged_in
def rating_vs_abv():
    return json_response(stats.rating_vs_abv)

@app.route('/api/checkin-locations')
@fail_unless_logged_in
def checkin_locations():
    return json_response(stats.checkin_locations)

@app.route('/api/basic')
@fail_unless_logged_in
def stats_basic():
    return json_response(stats.basic)

@app.route('/api/per-month')
@fail_unless_logged_in
def stats_per_month():
    return json_response(stats.per_month)
