import json
from httplib2 import Http
import datetime
from beertistics import app

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"


def update_last_indexed(username, datatype):
    pass


def get_last_indexed(username, datatype):
    return None


def is_current(username, datatype):
    return True


def index(datatype, items):
    pass


def search(datatype, query={}):
    return _default_result(datatype)


def get(datatype, id):
    return _default_result(datatype)


def _default_result(datatype):
    with open("stub/valle/%s.json" % datatype) as f:
        return json.load(f)
