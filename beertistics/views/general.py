import flask
from flask import g

import beertistics.auth as auth
from beertistics import app

@app.route('/')
def index():
    return flask.render_template('index.html', token=auth.get_token())

@app.route('/settings')
@auth.requires_auth
def settings():
    return flask.render_template('settings.html')

@app.route('/json/test')
@auth.requires_auth
def json_test():
    json = """
    {
      "meta": {
        "code": 200,
        "response_time": {
          "time": 0.248,
          "measure": "seconds"
        }
      },
      "notifications": [],
      "response": {
        "user": {
          "uid": 141680,
          "id": 141680,
          "user_name": "valle",
          "first_name": "Kjetil",
          "last_name": "V.",
        }
      }
    }
    """
    return flask.Response(json, 200, {'content-type': 'text/plain'})
