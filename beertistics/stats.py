import httplib2
from json import loads, load
import datetime
from beertistics import auth, cache, untappd
import flask
from collections import Counter
from beertistics import app

def basic():
    def days_since(date_str):
        then = datetime.datetime.strptime(date_str, untappd.DATE_FORMAT)
        now = datetime.datetime.now()
        delta = now - then
        return delta.days
    data = untappd.get_user_info()
    days = days_since(data['response']['user']['date_joined'])
    total = data['response']['user']['stats']['total_checkins']
    distinct = data['response']['user']['stats']['total_beers']
    return {
        "name": data['response']['user']['first_name'],
        "days": days,
        "date": data['response']['user']['date_joined'],
        "total": total,
        "distinct": distinct,
        "badges": data['response']['user']['stats']['total_badges'],
        "friends": data['response']['user']['stats']['total_friends'],
        "photos": data['response']['user']['stats']['total_photos'],
        "total_avg": "%.3f" % (float(total) / days),
        "distinct_avg": "%.3f" % (float(distinct) / days)
    }

def places():
    venues = [checkin["venue"]["venue_name"] 
                for checkin in untappd.get_checkins() 
                if checkin["venue"]]
    return [ 
      {
        "key": 'Number of checkins',
        "values": [{"label": venue, "value": n} for venue, n in Counter(venues).most_common(20)]
      }
    ]

def per_month():
    checkins = untappd.get_checkins()
    beers = set()
    new = dict()
    old = dict()
    months = set()
    for checkin in checkins:
        date = datetime.datetime.strptime(checkin["created_at"], untappd.DATE_FORMAT)
        month = date.strftime("%b %Y")
        month_sortable = date.strftime("%Y-%m")
        months.add((month_sortable, month))

        beer = checkin['beer']['bid']
        if beer in beers:
            old[month] = old.get(month, 0) + 1
        else:
            new[month] = new.get(month, 0) + 1
        beers.add(beer)

    sorted_months = [k[1] for k in sorted(months)]

    def mk_value_list(d):
        return [{"month": month, "beers": d.get(month, 0)} for month in sorted_months]

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
