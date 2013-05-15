from beertistics import untappd, search
import flask

def all(username=None):
    if not username:
        username = flask.session['shown_user']['username']

    if not search.is_current(username, "checkin"):
        search.index("checkin", untappd.get_checkins(username))
        search.update_last_indexed(username, "checkin")

    return search.search("checkin", {"term": {"user.user_name": username}})
