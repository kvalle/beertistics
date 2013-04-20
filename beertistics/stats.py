import httplib2
from json import loads, load
import datetime
from beertistics import auth, cache, untappd
import flask
from collections import Counter, defaultdict
from beertistics import app
from util import ensure_http_prefix

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

def test():
    return untappd.get_checkins()

def beers_by_country():
    countries = [c["brewery"]["country_name"] for c in untappd.get_checkins() if c["brewery"]]
    return [{
        "key": "Beers drunk from country",
        "values": [{"value": value, "label": label} for label, value in Counter(countries).most_common()]
    }]

def map_checkins():
    checkins = filter(lambda c: c["venue"], untappd.get_checkins())
    venues = dict((c["venue"]["venue_id"], { "name": c["venue"]["venue_name"],
                                                    "lat": c["venue"]["location"]["lat"], 
                                                    "lng": c["venue"]["location"]["lng"],
                                                    "url": ensure_http_prefix(c["venue"]["contact"]["venue_url"]),
                                                    "label": c["venue"]["venue_icon"]["sm"],
                                                    "beers_desc": "Beers drunk here:",
                                                    "beers": []})
                    for c in checkins)
    for c in checkins:
        beer = "%s by %s" % (c["beer"]["beer_name"], c["brewery"]["brewery_name"])
        venues[c["venue"]["venue_id"]]["beers"].append(beer)
    for bid in venues:
        venues[bid]["beers"] = list(set(venues[bid]["beers"]))
    return venues.values()

def map_breweries():
    checkins = filter(lambda c: c["brewery"] 
                            and c["brewery"]["location"]["lat"] 
                            and c["brewery"]["location"]["lng"],
                        untappd.get_checkins())
    breweries = dict((c["brewery"]["brewery_id"], { "name": c["brewery"]["brewery_name"],
                                                    "lat": c["brewery"]["location"]["lat"], 
                                                    "lng": c["brewery"]["location"]["lng"],
                                                    "url": ensure_http_prefix(c["brewery"]["contact"]["url"]),
                                                    "label": c["brewery"]["brewery_label"],
                                                    "beers_desc": "You\'ve tasted:",
                                                    "beers": []})
                    for c in checkins)
    for c in checkins:
        breweries[c["brewery"]["brewery_id"]]["beers"].append(c["beer"]["beer_name"])
    for bid in breweries:
        breweries[bid]["beers"] = list(set(breweries[bid]["beers"]))
    return breweries.values()

def rating_distribution():
    checkins = untappd.get_checkins()

    all_ratings = [checkin["rating_score"] for checkin in checkins if checkin["rating_score"]]
    total_counter = Counter(all_ratings)

    beers = set()
    distinct_ratings = []
    for checkin in checkins:
        if not checkin["beer"]["bid"] in beers:
            distinct_ratings.append(checkin["rating_score"])
            beers.add(checkin["beer"]["bid"])
    distinct_counter = Counter(distinct_ratings)
    
    keys = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    return [
        {
            "key": "Total",
            "values": [{"rating": rating, "n": total_counter[rating]} for rating in keys]
        },
        {
            "key": "Distinct",
            "values": [{"rating": rating, "n": distinct_counter[rating]} for rating in keys]
        }
    ]

def time_of_day():
    dates = [datetime.datetime.strptime(checkin["created_at"], untappd.DATE_FORMAT) 
                for checkin in untappd.get_checkins()]
    tuples = [(d.weekday(), d.hour) for d in dates]
    return [{
        "key": "Time and day",
        "values": [{"weekday": weekday, "hour": hour, "size": size} 
                    for (weekday, hour), size in Counter(tuples).most_common()]
    }]

def rating_vs_abv():
    tuples = [(checkin["rating_score"], checkin["beer"]["beer_abv"]) 
                for checkin in untappd.get_checkins() 
                if checkin["rating_score"] and checkin["beer"]["beer_abv"]]
    return [{
        "key": "Rating vs ABV",
        "values": [{"abv": abv, "rating": rating, "size": size} 
                    for (rating, abv), size in Counter(tuples).most_common()]
    }]

def checkin_locations():
    venues = [checkin["venue"]["venue_name"] 
                for checkin in untappd.get_checkins() 
                if checkin["venue"]]
    return [ 
      {
        "key": 'Number of checkins',
        "values": [{"label": venue, "value": n} for venue, n in Counter(venues).most_common()]
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
