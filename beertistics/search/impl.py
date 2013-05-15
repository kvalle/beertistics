import json
from httplib2 import Http
import datetime
from beertistics import app

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"


def update_last_indexed(username, datatype):
    data = get("cache", username)
    if data:
        data[datatype] = datetime.datetime.now().strftime(DATE_FORMAT)
    else:
        data = {datatype: datetime.datetime.now().strftime(DATE_FORMAT)}

    url = "http://localhost:9200/beertistics/cache/%s" % username
    resp, content = Http().request(url, "POST", json.dumps(data))


def get_last_indexed(username, datatype):
    url = "http://localhost:9200/beertistics/cache/%s" % username
    resp, content = Http().request(url, "GET")
    try:
        t = json.loads(content)["_source"][datatype]
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
    url = "http://localhost:9200/beertistics/%s" % datatype
    http = Http()
    for item in items:
        resp, content = http.request(url, "POST", json.dumps(item))
    http.request("http://localhost:9200/beertistics/_refresh", "POST")


def search(datatype, query={}):
    url = "http://localhost:9200/beertistics/%s/_search" % datatype
    data = {"query": query, "size": 100000}
    resp, content = Http().request(url, "POST", json.dumps(data))
    result = json.loads(content)
    return [hit["_source"] for hit in result["hits"]["hits"]]


def get(datatype, id):
    url = "http://localhost:9200/beertistics/%s/%s" % (datatype, id)
    resp, content = Http().request(url, "GET")
    data = json.loads(content)
    return data["_source"] if data["exists"] else None
