#!/usr/bin/env python

import json

from flask.ext.script import Manager, prompt_bool
from beertistics import app, search

manager = Manager(app, with_default_commands=False, \
    usage="Perform operations on Elastic Search")

@manager.command
def es_clear_index():
    """Clear all data from Elastic Search indexes"""
    if prompt_bool("Really clean index?"):
        print json.dumps(search.clear_index(), indent=4)

@manager.command
def es_status():
    """Display status info for Elastic Search"""
    print json.dumps(search.status(), indent=4)

