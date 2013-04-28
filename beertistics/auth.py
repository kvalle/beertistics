from functools import wraps
import flask
from beertistics import untappd, app, user_service

def authorize(code):
    token = untappd.authorize(code)

    if not token:
        return False
    
    flask.session['untappd_token'] = token
    user = user_service.user_basis_info()
    flask.session['logged_in_user'] = user
    flask.session['shown_user'] = user
    flask.session['user_suggestions'] = user_service.user_friends()

    app.logger.info('%s logged in' % flask.session['logged_in_user']["username"])
    return True

def is_logged_in():
    return 'untappd_token' in flask.session

def logout():
    flask.session.pop('untappd_token', None)
    flask.session.pop('logged_in_user', None)
    flask.session.pop('show_for_username', None)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            flask.session['next_page'] = flask.request.url
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
