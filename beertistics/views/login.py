import flask
from flask import g

import beertistics.auth as auth
from beertistics import app

@app.route('/log-in', methods=['GET', 'POST'])
def login():
    username = ""
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        if auth.login(username, password):
            flask.flash('You were logged in.', 'success')
            next_page = flask.session.pop('next_page', flask.url_for('index'))
            return flask.redirect(next_page)
        else:
            flask.flash('Invalid username or password.', 'error')
    return flask.render_template('login.html', username=username)

@app.route('/log-out')
def logout():
    auth.logout()
    flask.flash('You were logged out.', 'success')
    return flask.redirect(flask.url_for('login'))

