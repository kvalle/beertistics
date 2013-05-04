from beertistics import untappd, search
import datetime
import flask

##
## Helper functions
##

def _days_since(date_str):
    then = datetime.datetime.strptime(date_str, untappd.DATE_FORMAT)
    now = datetime.datetime.now()
    delta = now - then
    return delta.days

def _refresh_user_info(username):
    if not search.is_current(username, "user_info"):
        data = untappd.get_user_info(username)
        search.index("user_info", [data])
        search.update_last_indexed(username, "user_info")

def _basis(info):
    user = info['response']['user']
    full_name = "%s %s" % (user['first_name'], user['last_name'])
    days = _days_since(user['date_joined'])
    total = user['stats']['total_checkins']
    distinct = user['stats']['total_beers']
    return {
        'name': full_name.strip(),
        'username': user['user_name'],
        'avatar': user['user_avatar'],
        'url': user['untappd_url'],
        "days": days,
        "date": user['date_joined'],
        "total": total,
        "avatar": user['user_avatar'],
        "distinct": distinct,
        "badges": user['stats']['total_badges'],
        "friends": user['stats']['total_friends'],
        "photos": user['stats']['total_photos'],
        "total_avg": "%.3f" % (float(total) / days),
        "distinct_avg": "%.3f" % (float(distinct) / days)
    }

##
## user_info functions
##

def user_info_for(username):
    _refresh_user_info(username)
    info = search.get("user_info", username)
    return _basis(info)

def user_info_for_logged_in_user():
    if flask.session.get("logged_in_user", False):
        return user_info_for(flask.session["logged_in_user"]["username"])

    data = untappd.get_user_info()
    search.index("user_info", [data])
    info = _basis(data)
    search.update_last_indexed(info["username"], "user_info")
    return info
    
##
## user_friends functions
##

def friend_list_for(username):
    if not search.is_current(username, "friend_list"):
        data = untappd.get_user_friends(username)
        friends = [friend["user"]["user_name"] for friend in data]
        search.index("friend_list", [{"user": username, "friends": friends}])
        search.update_last_indexed(username, "friend_list")

    return search.get("friend_list", username)["friends"]
