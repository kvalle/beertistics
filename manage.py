#!/usr/bin/env python

import json

from flask.ext.script import Manager
from beertistics import app

from manage_es import manager as es

manager = Manager(app)

@manager.command
def hello():
    print "hello, I'm your friendly neighborhood manager script"

if __name__ == "__main__":
    manager.add_command("es", es)
    manager.run()
