from beertistics import untappd, cache

@cache.cached("user_info")
def info(user=None):
    return untappd.get_user_info(user)