from beertistics import app, util
import os.path
import os 
import flask
from datetime import datetime, timedelta
import json

CACHE_FILE = app.config['BASE_DIR']+"/cache.db"

def make_key(username):
    if username: 
        return util.normalize(username)

    if "logged_in_user" in flask.session and "username" in flask.session["logged_in_user"]:
        username = flask.session["logged_in_user"]["username"]
        return util.normalize(username)

    return False

def cached(key):
    def cache_fn(fn):
        def wrapper(username=None):  
            username = make_key(username)
            if not username:
                return fn(username)

            cache_file = "%s/%s_%s.json" % (app.config["CACHE_DIR"], username, key)

            def is_current(cache_file):
                if not os.path.exists(cache_file):
                    return False

                ttl = timedelta(0, app.config["CACHE_TTL"])
                age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))

                return age < ttl

            if is_current(cache_file):
                with open(cache_file, "r") as f:
                    return json.load(f)
            else:
                app.logger.info('cache miss for %s/%s, retrieving' % (username, key))
                data = fn(username)
                with open(cache_file, "w") as f:
                    json.dump(data, f)
                return data

        return wrapper
    return cache_fn

def clear(username):
    username = make_key(username)
    try:
        for cache_file in os.listdir(app.config["CACHE_DIR"]):
            if cache_file.startswith(username + "_"):
                file_path = os.path.join(app.config["CACHE_DIR"], cache_file)
                os.unlink(file_path)
        app.logger.info("cleared cache for '%s'" % username)
    except Exception, e:
        print e
