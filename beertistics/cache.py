from beertistics import auth, app
import shelve

CACHE_FILE = app.config['BASE_DIR']+"/cache.db"

def cached(key):
    def cache_fn(fn):
        def wrapper():  
            stored = shelve.open(CACHE_FILE)

            username = auth.username()

            if not stored.has_key(username):
                stored[username] = {}

            if key in stored[username]:
                return stored[username][key]
            else:
                cache = stored[username]
                cache[key] = fn()
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