from beertistics import untappd, cache

@cache.cached("user_info")
def all_user_data(username=None):
    return untappd.get_user_info(username)

def user_stats(username=None):
    pass # TODO

def user_basis_info(username=None):
    info = all_user_data(username)
    if not info: 
        return False
    user = info['response']['user']
    full_name = "%s %s" % (user['first_name'], user['last_name'])
    return {
        'name': full_name.strip(),
        'username': user['user_name'],
        'avatar': user['user_avatar'],
        'url': user['untappd_url']
    }