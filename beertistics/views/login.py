import flask
from flask import g

from beertistics import app, auth, cache, untappd

@app.route('/auth')
def authentication():
    """
        Callback URI for Untappd authentication.
        Should only be called as callback from Untappd OAuth.
    """
    code = flask.request.args.get('code', False)

    if code and auth.authorize(code):
        flask.flash('You were successfully logged in.', 'success')
        return flask.redirect(flask.url_for('login'))

    else:
        flask.flash('Authentication with Untappd failed.', 'error')
        return flask.redirect(flask.url_for('index'))    

@app.route('/log-in')
def login():
    if not auth.is_logged_in():
        return flask.redirect(untappd.authenticate_url())

    next_page = flask.session.pop('next_page', flask.url_for('index'))
    return flask.redirect(next_page) 

@app.route('/log-out')
def logout():
    cache.clear()
    auth.logout()
    flask.flash('You were logged out.', 'success')
    return flask.redirect(flask.url_for('index'))

