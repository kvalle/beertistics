from beertistics import app, util
import flask
import shelve

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

            if key in stored[username]:
                return stored[username][key]
            else:
                cache = stored[username]
                cache[key] = fn(username)
                stored[username] = cache
                return stored[username][key]
        return wrapper
    return cache_fn

def clear(username=None):
    stored = shelve.open(CACHE_FILE)
    if username:
        if stored.has_key(username):
            del stored[username]
    else:
        stored.clear()