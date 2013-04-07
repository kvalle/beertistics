from flask import Flask, render_template, g
import config

app = Flask(__name__)
app.config.from_object(config)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from beertistics.views import general
from beertistics.views import login
from beertistics.views import api
