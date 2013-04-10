import unicodedata
import flask

def normalize(string):
    return unicodedata.normalize('NFKD', string).encode('ascii','ignore')

def ensure_http_prefix(url):
    if url and url[:7] != ("http://"):
        return "http://%s" % url
    else:
        return url