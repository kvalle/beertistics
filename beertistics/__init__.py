from flask import Flask, render_template
from logging.handlers import RotatingFileHandler
import logging
import os

app = Flask(__name__)

try:
    config = os.environ["BEERTISTICS_CONFIG"]
except:
    config = "default"

app.config.from_object("beertistics.config.%s" % config)

log_file = app.config['BASE_DIR'] + '/logs/beertistics.log'
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler = RotatingFileHandler(log_file, 'a+', 1 * 1024 * 1024, 10)
file_handler.setFormatter(log_formatter)
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

import beertistics.views  # noqa
