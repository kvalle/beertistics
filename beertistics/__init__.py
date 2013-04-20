from flask import Flask, render_template, g
from logging.handlers import RotatingFileHandler
import logging
import os

app = Flask(__name__)

try:
    config = os.environ["BEERTISTICS_CONFIG"]
except:
    config = "default"

app.logger.info("Loading %s config" % config)
app.config.from_object("beertistics.config.%s" % config)

file_handler = RotatingFileHandler(app.config['BASE_DIR']+'/logs/beertistics.log', 'a+', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('beertistics startup')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

import beertistics.views
