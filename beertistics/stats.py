import httplib2
from json import loads, load
import datetime
from beertistics import auth, cache, untappd
import flask
from beertistics import app

def basic():
    json = untappd.get_user_info()
    user = json['response']['user']
    stats = user['stats']
    days = days_since(user['date_joined'])
    total = stats['total_checkins']
    distinct = stats['total_beers']
    return {
        "name": user['first_name'],
        "days": days,
        "date": user['date_joined'],
        "total": total,
        "distinct": distinct,
        "badges": stats['total_badges'],
        "friends": stats['total_friends'],
        "photos": stats['total_photos'],
        "total_avg": "%.3f" % (float(total) / days),
        "distinct_avg": "%.3f" % (float(distinct) / days)
    }

def per_month():
    checkins = untappd.get_checkins()
    beers = set()
    new = dict()
    old = dict()
    keys = set()
    for checkin in checkins:
        date = datetime.datetime.strptime(checkin["created_at"], untappd.DATE_FORMAT)
        key = date.strftime("%b %Y")
        key_sortable = date.strftime("%Y-%m")
        keys.add((key_sortable, key))

        beer = checkin['beer']['bid']
        if beer in beers:
            old[key] = old.get(key, 0) + 1
        else:
            new[key] = new.get(key, 0) + 1
        beers.add(beer)

    sorted_keys = [k[1] for k in sorted(keys)]

    def mk_value_list(d):
        return [{"x": key, "y": d.get(key, 0)} for key in sorted_keys]

    return [
        { 
            "key": "New tastings",
            "values": mk_value_list(new)
        }, {
            "key": "Beers tasted before",
            "values": mk_value_list(old)
        }
    ]

def photos():
    def has_photo(checkin):
        return checkin["media"]["count"] > 0
    def pick_data(checkin):
        return {
            "photo": checkin["media"]["items"][0]["photo"]["photo_img_md"],
            "photo_original": checkin["media"]["items"][0]["photo"]["photo_img_og"],
            "comment": checkin["checkin_comment"],
            "beer": checkin["beer"]["beer_name"],
            "brewery": checkin["brewery"]["brewery_name"],
            "rating": checkin["rating_score"]
        }
    return map(pick_data, filter(has_photo, untappd.get_checkins()))

def days_since(date_str):
    then = datetime.datetime.strptime(date_str, untappd.DATE_FORMAT)
    now = datetime.datetime.now()
    delta = now - then
    return delta.days