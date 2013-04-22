import flask
from beertistics import app, auth

@app.route('/stats/beers-by-country')
@auth.requires_auth
def stats_beers_by_country():
    return flask.render_template('stats/beers-by-country.html')

@app.route('/stats/country-chart')
@auth.requires_auth
def stats_country_chart():
    return flask.render_template('stats/country-chart.html')

@app.route('/stats/consumption-per-month')
@auth.requires_auth
def stats_consumption_per_month():
    return flask.render_template('stats/consumption-per-month.html')

@app.route('/stats/checkin-locations')
@auth.requires_auth
def stats_checkin_locations():
    return flask.render_template('stats/checkin-locations.html')

@app.route('/stats/rating-distribution')
@auth.requires_auth
def stats_rating_distribution():
    return flask.render_template('stats/rating-distribution.html')

@app.route('/stats/rating-vs-abv')
@auth.requires_auth
def stats_rating_vs_abv():
    return flask.render_template('stats/rating-vs-abv.html')

@app.route('/stats/punchcard')
@auth.requires_auth
def stats_punchcard():
    return flask.render_template('stats/punchcard.html')

@app.route('/stats/overview')
@auth.requires_auth
def stats_overview():
    return flask.render_template('stats/index.html')