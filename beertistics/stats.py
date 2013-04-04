import httplib2
from json import loads, load
import datetime
from beertistics import auth, cache
import flask
from beertistics import app

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def days_since(date_str):
    then = datetime.datetime.strptime(date_str, DATE_FORMAT)
    now = datetime.datetime.now()
    delta = now - then
    return delta.days

@cache.memoize(timeout=app.config['CACHE_TIMEOUT'])
def get_stats(url):
    _, content = httplib2.Http().request(url)
    return loads(content)

def basic():
    # TODO: consider just sending html instead
    url = "http://api.untappd.com/v4/user/info?" + auth.get_url_params()
    json = get_stats(url)
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

def get_month(checkin):
    return "Apr 2013"

def per_month():
    checkins = get_all_checkins()
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

def get_sample_checkins():
    with open("beertistics/test.json") as f:
        return load(f)

def get_all_checkins():
    checkins = []
    url = "http://api.untappd.com/v4/user/checkins?" + auth.get_url_params()
    json = get_stats(url)
    
    checkins += json["response"]["checkins"]["items"]
    next = json["response"]["pagination"]["next_url"]
    while next:
        next += auth.get_url_params()
        print next
        json = get_stats(next)
        checkins += json["response"]["checkins"]["items"]
        next = json["response"]["pagination"]["next_url"]

    return checkins
