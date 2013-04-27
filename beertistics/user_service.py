from beertistics import untappd, cache

@cache.cached("user_info")
def full_user_info(user=None):
    return untappd.get_user_info(user)

def get_logged_in_user():
    info = full_user_info()
    user = info['response']['user']
    return {
        'name': "%s %s" % (user['first_name'], user['last_name']),
        'username': user['user_name'],
        'avatar': user['user_avatar'],
        'url': user['untappd_url']
    }