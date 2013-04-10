import flask
from beertistics import app, auth

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.render_template('index.html')
    else:
        return flask.render_template('login.html')

@app.route('/photos')
def photos():
    return flask.render_template('photos.html')

@app.route('/map')
def map():
    return flask.render_template('map.html')

@app.route('/about')
def about():
    return flask.render_template('about.html')
