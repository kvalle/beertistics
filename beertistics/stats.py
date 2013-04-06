import httplib2
from json import loads, load
import datetime
from beertistics import auth
import flask
import shelve
from beertistics import app
import unicodedata

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def cached(key):
    def cache_fn(fn):
        stored = shelve.open("cache.db")
        def wrapper():
            username = unicodedata.normalize('NFKD', flask.session["user"]["username"]).encode('ascii','ignore')
            cache_key = username+"_"+key
            if stored.has_key(cache_key):
                return stored[cache_key]
            else:
                stored[cache_key] = fn()
                return stored[cache_key]
        return wrapper
    return cache_fn

def get(url):
    print "FETCHING: " + url
    _, content = httplib2.Http().request(url)
    return loads(content)

@cached("user_info")
def get_user_info():
    return get("http://api.untappd.com/v4/user/info?" + auth.get_url_params())

@cached("checkins")
def get_checkins():
    json = get("http://api.untappd.com/v4/user/checkins?" + auth.get_url_params())

    checkins = json["response"]["checkins"]["items"]
    next = json["response"]["pagination"]["next_url"]
    while next:
        next += auth.get_url_params()
        print next
        json = get(next)
        checkins += json["response"]["checkins"]["items"]
        next = json["response"]["pagination"]["next_url"]

    return checkins

def get_checkins_stub():
    with open("beertistics/test.json") as f:
        return load(f)

def basic():
    json = get_user_info()
    user = json['response']['user']
    stats = user['stats']
    days = days_since(user['date_joined'])
    total = stats['total_checkins']
    distinct = stats['total_beers']
    return {
        "beers": {
            "distinct beers drunk": distinct,
            "total beers drunk": total,
            "average beers per day": "%.3f" % (float(total) / days),
            "average new distinct beers per day": "%.3f" % (float(distinct) / days)
        },
        "misc": {
            "days since the drinking began": days,
            "badges received": stats['total_badges'],
            "new brews registered to Untappd": stats['total_created_beers'],
            "photos upladed": stats['total_photos'],
            "friends on Untappd": stats['total_friends']
        }
    }

def per_month():
    checkins = get_checkins_stub()
    beers = set()
    new = dict()
    old = dict()
    keys = set()
    for checkin in checkins:
        date = datetime.datetime.strptime(checkin["created_at"], DATE_FORMAT)
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
    return map(pick_data, filter(has_photo, get_sample_checkins()))

def days_since(date_str):
    then = datetime.datetime.strptime(date_str, DATE_FORMAT)
    now = datetime.datetime.now()
    delta = now - then
    return delta.days