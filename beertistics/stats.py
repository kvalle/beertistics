import httplib2
from json import loads
import datetime
from beertistics import auth
import flask

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def days_since(date_str):
    then = datetime.datetime.strptime(date_str, DATE_FORMAT)
    now = datetime.datetime.now()
    delta = now - then
    return delta.days

def basic():
    # TODO: consider just sending html instead
    url = "http://api.untappd.com/v4/user/info" + auth.get_url_params()
    resp, content = httplib2.Http().request(url)
    json = loads(content)
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
    return [
      {
        "key":"New beers",
        "values": [{"x":"mar 2012","y":31},
                   {"x":"apr 2012","y":42},
                   {"x":"may 2012","y":53},
                   {"x":"jun 2012","y":25},
                   {"x":"jul 2012","y":15},
                   {"x":"aug 2012","y":12},
                   {"x":"sep 2012","y":35},
                   {"x":"oct 2012","y":25},
                   {"x":"nov 2012","y":15},
                   {"x":"dec 2012","y":16},
                   {"x":"jan 2012","y":12},
                   {"x":"feb 2013","y":6}]
      }, {
        "key":"Beers tasted before",
        "values": [{"x":"mar 2012","y":12},
                   {"x":"apr 2012","y":31},
                   {"x":"may 2012","y":51},
                   {"x":"jun 2012","y":12},
                   {"x":"jul 2012","y":6},
                   {"x":"aug 2012","y":31},
                   {"x":"sep 2012","y":12},
                   {"x":"oct 2012","y":15},
                   {"x":"nov 2012","y":15},
                   {"x":"dec 2012","y":12},
                   {"x":"jan 2012","y":19},
                   {"x":"feb 2013","y":27}]
      }
    ]