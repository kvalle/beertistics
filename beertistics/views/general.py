import flask
from beertistics import app, auth

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.redirect(flask.url_for("stats_overview"))
    else:
        return flask.render_template('login.html')

@app.route('/test')
@auth.requires_auth
def test():
    return flask.render_template('test.html')

@app.route('/photos')
@auth.requires_auth
def photos():
    return flask.render_template('photos.html')

@app.route('/map')
@auth.requires_auth
def map():
    return flask.render_template('map.html')

@app.route('/about')
@auth.requires_auth
def about():
    return flask.render_template('about.html')
