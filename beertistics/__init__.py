from flask import Flask, render_template, g
import config

app = Flask(__name__)
app.config.from_object(config)

import logging
from logging.handlers import RotatingFileHandler
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
