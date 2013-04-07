import unicodedata
import flask

def normalize(string):
    return unicodedata.normalize('NFKD', string).encode('ascii','ignore')