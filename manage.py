#!/usr/bin/env python

import json

from flask.ext.script import Manager, prompt_bool
from beertistics import app, search

manager = Manager(app)

@manager.command
def es_clear_index():
    if prompt_bool("Really clean index?"):
        print json.dumps(search.clear_index(), indent=4)

@manager.command
def es_status():
    print json.dumps(search.status(), indent=4)

if __name__ == "__main__":
    manager.run()
