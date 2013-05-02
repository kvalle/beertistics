from beertistics import untappd, search

def all(username):
    if not search.is_current(username, "checkin"):
        search.index("checkin", untappd.get_checkins(username))
        search.update_last_indexed(username, "checkin")

    return search.search({"term":{"user.user_name": username}})