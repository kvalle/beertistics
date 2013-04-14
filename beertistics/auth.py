from functools import wraps
import flask
from beertistics import untappd

def authorize(code):
    token = untappd.authorize(code)

    if not token:
        return False
    
    flask.session['untappd_token'] = token
    flask.session['logged_in'] = True

    info = untappd.get_user_info()
    user = info['response']['user']
    flask.session['user'] = {
        'name': "%s %s" % (user['first_name'], user['last_name']),
        'username': user['user_name'],
        'avatar': user['user_avatar'],
        'url': user['untappd_url']
    }
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
