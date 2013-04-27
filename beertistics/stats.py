import httplib2
from json import loads, load
from datetime import timedelta, datetime
from calendar import month_abbr as months
from beertistics import untappd, user_service, checkins_service
from collections import Counter, defaultdict
from util import ensure_http_prefix

def basic():
    def days_since(date_str):
        then = datetime.strptime(date_str, untappd.DATE_FORMAT)
        now = datetime.now()
        delta = now - then
        return delta.days
    data = user_service.full_user_info()
    days = days_since(data['response']['user']['date_joined'])
    total = data['response']['user']['stats']['total_checkins']
    distinct = data['response']['user']['stats']['total_beers']
    return {
        "name": data['response']['user']['first_name'],
        "days": days,
        "date": data['response']['user']['date_joined'],
        "total": total,
        "avatar": data['response']['user']['user_avatar'],
        "distinct": distinct,
        "badges": data['response']['user']['stats']['total_badges'],
        "friends": data['response']['user']['stats']['total_friends'],
        "photos": data['response']['user']['stats']['total_photos'],
        "total_avg": "%.3f" % (float(total) / days),
        "distinct_avg": "%.3f" % (float(distinct) / days)
    }

def test():
    return checkins_service.all()

def influenced_ratings():
    dt = lambda string: datetime.strptime(string, untappd.DATE_FORMAT)
    checkins = [(dt(c["created_at"]), c["rating_score"]) for c in checkins_service.all()]
    data = []
    for c in checkins:
        is_recent = lambda (t,r): timedelta(0) < (c[0] - t) < timedelta(0, 6*60*60)
        num = len(filter(is_recent, checkins))
        data.append((num, c[1]))
    return [{
        "key": "Rating under the influence",
        "values": [{"rating": rating, "beers": beers, "size": size} 
                    for (beers, rating), size in Counter(data).most_common()]
    }]

def beers_by_country():
    countries = [c["brewery"]["country_name"] for c in checkins_service.all() if c["brewery"]]
    return [{
        "key": "Beers drunk from country",
        "values": [{"value": value, "label": label} for label, value in Counter(countries).most_common()]
    }]

def beers_by_country_as_list():
    countries = [c["brewery"]["country_name"] for c in checkins_service.all() if c["brewery"]]
    fix_gb = lambda country: "Great Britain" if country in ["Scotland", "England", "Wales"] else country
    countries = map(fix_gb, countries) # Google geo charts only support GB, not the sub-divisions
    return [['Country', 'Beers tasted']] + \
         [[country, count] for country, count in Counter(countries).most_common()]

def map_checkins():
    checkins = filter(lambda c: c["venue"], checkins_service.all())
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
                        checkins_service.all())
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
    checkins = checkins_service.all()

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
    dates = [datetime.strptime(checkin["created_at"], untappd.DATE_FORMAT) 
                for checkin in checkins_service.all()]
    tuples = [(d.weekday(), d.hour) for d in dates]
    return [{
        "key": "Time and day",
        "values": [{"weekday": weekday, "hour": hour, "size": size} 
                    for (weekday, hour), size in Counter(tuples).most_common()]
    }]

def rating_vs_abv():
    tuples = [(checkin["rating_score"], checkin["beer"]["beer_abv"]) 
                for checkin in checkins_service.all() 
                if checkin["rating_score"] and checkin["beer"]["beer_abv"]]
    return [{
        "key": "Rating vs ABV",
        "values": [{"abv": abv, "rating": rating, "size": size} 
                    for (rating, abv), size in Counter(tuples).most_common()]
    }]

def checkin_locations():
    venues = [checkin["venue"]["venue_name"] 
                for checkin in checkins_service.all() 
                if checkin["venue"]]
    return [ 
      {
        "key": 'Number of checkins',
        "values": [{"label": venue, "value": n} for venue, n in Counter(venues).most_common()]
      }
    ]

def per_month():
    checkins = checkins_service.all()
    beers = set()
    new = defaultdict(int)
    old = defaultdict(int)
    keys = set()
    for checkin in checkins:
        date = datetime.strptime(checkin["created_at"], untappd.DATE_FORMAT)
        key = (int(date.strftime("%Y")), int(date.strftime("%m")))
        keys.add(key)

        beer = checkin['beer']['bid']
        if beer in beers:
            old[key] = old[key] + 1
        else:
            new[key] = new[key] + 1
        beers.add(beer)

    def make_key_list(curr, end):
        keys = [curr]
        while curr < end:
            (y, m) = curr
            curr = (y+1, 1) if m == 12 else (y, m+1)
            keys.append(curr)
        return keys

    keys = make_key_list(min(keys), max(keys))

    def mk_value_list(d):
        return [{"month": "%s %s" % (months[month], year), "beers": d.get((year, month), 0)} 
                    for year, month in keys]

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
    return map(pick_data, filter(has_photo, checkins_service.all()))
