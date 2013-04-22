import flask
from beertistics import app, auth, cache

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.render_template('index.html')
    else:
        return flask.render_template('login.html')

@app.route('/clear')
@auth.requires_auth
def clear():
    username = flask.session['user']['username']
    cache.clear(username)
    flask.flash("Cleared cache for \"%s\"" % username, "success")
    return flask.redirect(flask.url_for("index"))

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
