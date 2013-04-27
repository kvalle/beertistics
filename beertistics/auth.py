from functools import wraps
import flask
from beertistics import untappd, app, user

def authorize(code):
    token = untappd.authorize(code)

    if not token:
        return False
    
    flask.session['untappd_token'] = token
    flask.session['logged_in'] = True

    info = user.info()
    logged_in_user = info['response']['user']
    flask.session['user'] = {
        'name': "%s %s" % (logged_in_user['first_name'], logged_in_user['last_name']),
        'username': logged_in_user['user_name'],
        'avatar': logged_in_user['user_avatar'],
        'url': logged_in_user['untappd_url']
    }
    app.logger.info('%s logged in' % logged_in_user["user_name"])
    return True

def get_token():
    return flask.session.get('untappd_token', None)

def is_logged_in():
    return 'untappd_token' in flask.session

def logout():
    flask.session.pop('untappd_token', None)
    flask.session['logged_in'] = False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            flask.session['next_page'] = flask.request.url
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
