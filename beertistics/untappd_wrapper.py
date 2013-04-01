import httplib2
from json import loads, dumps
from functools import wraps
import flask
from beertistics import app

def prettify(content):
    return dumps(content, indent=4)

def user_info():
    url = "http://api.untappd.com/v4/user/info?client_id=C2B98311257562CC0BA3505452861DD8DF65DCC6&client_secret=9180BCBA0DFC55C76E125673F4D9F7D9E4A8B324&access_token=CD4845AF9B4960FCCFC1BCEA6D2858E9CD6F667C"
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