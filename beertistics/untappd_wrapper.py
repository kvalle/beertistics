import httplib2
from json import loads, dumps
from functools import wraps
import flask
from beertistics import app
from beertistics import auth

def prettify(content):
    return dumps(content, indent=4)

def user_info():
    url = "http://api.untappd.com/v4/user/info" + auth.get_url_params()
    resp, content = httplib2.Http().request(url)
    json = loads(content)

    user = json['response']['user']
    data = {
        'name': "%s %s" % (user['first_name'], user['last_name']),
        'username': user['user_name'],
        'avatar': user['user_avatar'],
        'url': user['untappd_url']
    }
    return prettify(data)