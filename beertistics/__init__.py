from flask import Flask, render_template, g
from flask.ext.cache import Cache
import config

app = Flask(__name__)
app.config.from_object(config)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from beertistics.views import general
from beertistics.views import login
