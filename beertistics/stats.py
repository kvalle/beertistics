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
    checkins = get_sample_checkins()
    beers = set()
    new = dict()
    old = dict()
    for checkin in checkins:
        date = datetime.datetime.strptime(checkin["created_at"], DATE_FORMAT)
        month_name = date.strftime("%b")
        month_nr = date.strftime("%m")
        year = date.strftime("%Y")
        key = (year, month_nr, month_name)
        beer = checkin['beer']['bid']
        if beer in beers:
            old[key] = old.get(key, 0) + 1
        else:
            new[key] = new.get(key, 0) + 1
        beers.add(beer)

    def mk_value_list(d):
        return [
            {"x": key[2] + " " + key[0], "y": d[key]} 
            for key in sorted(d.keys())
        ]

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

def dummy_data():
    return [
    {
        "values": [
            { "y": 28, "x": "Jul 2012"}, 
            { "y": 11, "x": "Apr 2012"}, 
            { "y": 32, "x": "Nov 2012"}, 
            { "y": 29, "x": "Feb 2013"}, 
            { "y": 39, "x": "Dec 2012"}, 
            { "y": 31, "x": "Oct 2012"}, 
            { "y": 21, "x": "Jun 2012"}, 
            { "y": 38, "x": "Sep 2012"}, 
            { "y": 52, "x": "Mar 2013"}, 
            { "y": 2, "x": "Apr 2013"}, 
            { "y": 6, "x": "May 2012"}, 
            { "y": 36, "x": "Aug 2012"}, 
            { "y": 29, "x": "Jan 2013"}, 
            { "y": 28, "x": "Mar 2012"}
        ],
        "key": "New tastings"
    }, 
    {
        "values": [
            { "y": 9, "x": "Jul 2012" }, 
            { "y": 12, "x": "Apr 2012" }, 
            { "y": 20, "x": "Nov 2012" }, 
            { "y": 8, "x": "Feb 2013" }, 
            { "y": 11, "x": "Dec 2012" }, 
            { "y": 16, "x": "Oct 2012" }, 
            { "y": 18, "x": "Jun 2012" }, 
            { "y": 16, "x": "Sep 2012" }, 
            { "y": 5, "x": "Mar 2013" }, 
            { "y": 9, "x": "Mar 2012" }, 
            { "y": 6, "x": "May 2012" }, 
            { "y": 11, "x": "Aug 2012" }, 
            { "y": 6, "x": "Jan 2013" }
        ], 
        "key": "Beers tasted before"
    }
]