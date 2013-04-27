from beertistics import untappd, cache

@cache.cached("checkins")
def all(user=None):
    return untappd.get_checkins(user)
