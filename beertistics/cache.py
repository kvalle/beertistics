from beertistics import app, util
import flask
import shelve
from datetime import datetime, timedelta

CACHE_FILE = app.config['BASE_DIR']+"/cache.db"

def make_key(username):
    if username: 
        return util.normalize(username)

    if "user" in flask.session and "username" in flask.session["user"]:
        username = flask.session["user"]["username"]
        return util.normalize(username)

    return False

def cached(key):
    def cache_fn(fn):
        def wrapper(username=None):  
            stored = shelve.open(CACHE_FILE)

            username = make_key(username)

            if not username:
                return fn()

            if not stored.has_key(username):
                stored[username] = {}

            limit = timedelta(0, app.config["CACHE_TTL"])
            cache_hit = key in stored[username] \
                and (datetime.now() - stored[username][key]["time"]) < limit

            if cache_hit:
                return stored[username][key]["data"]
            else:
                app.logger.info('cache miss for %s/%s, retrieving' % (username, key))
                cache = stored[username]
                cache[key] = {}
                cache[key]["data"] = fn(username)
                cache[key]["time"] = datetime.now()
                stored[username] = cache
                return stored[username][key]["data"]
        return wrapper
    return cache_fn

def clear(username=None):
    stored = shelve.open(CACHE_FILE)
    username = make_key(username)
    if username:
        if stored.has_key(username):
            del stored[username]
            app.logger.info("cleared cache for '%s'" % username)
    else:
        stored.clear()
        app.logger.info('cleared cache')
