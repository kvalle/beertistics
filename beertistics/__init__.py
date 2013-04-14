from flask import Flask, render_template, g
import config

app = Flask(__name__)
app.config.from_object(config)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

import beertistics.views
