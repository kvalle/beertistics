import json
from httplib2 import Http
import datetime
from beertistics import app

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def update_last_indexed(username, datatype):
    url = "http://localhost:9200/beertistics/cache/%s" % username
    data = {datatype: datetime.datetime.now().strftime(DATE_FORMAT)}
    resp, content = Http().request(url, "POST", json.dumps(data))
    print content

def get_last_indexed(username, datatype):
    url = "http://localhost:9200/beertistics/cache/%s" % username
    resp, content = Http().request(url, "GET")
    try:
        t = json.loads(content)["_source"]["checkin"]
        return datetime.datetime.strptime(t, DATE_FORMAT)
    except:
        return None

def is_current(username, datatype):
    ttl = datetime.timedelta(0, app.config["CACHE_TTL"])

    last_indexed = get_last_indexed(username, datatype)
    if not last_indexed:
        return False

    delta = datetime.datetime.now() - last_indexed
    return delta < ttl

def index(datatype, items):
    url = "http://localhost:9200/beertistics/checkin"
    http = Http()
    for item in items:
        resp, content = http.request(url, "POST", json.dumps(item))
        print content
    http.request("http://localhost:9200/beertistics/_refresh", "POST")

def search(query={}):
    url = "http://localhost:9200/beertistics/checkin/_search"
    data = {"query": query, "size": 100000}
    resp, content = Http().request(url, "POST", json.dumps(data))
    result = json.loads(content)
    print "found %d checkins" % result["hits"]["total"]
    return [hit["_source"] for hit in result["hits"]["hits"]]
