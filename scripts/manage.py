#!/usr/bin/env python

import sys
import os.path
import json

# Add project root to python path, so we'll find beertistics
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir + "/..")

from beertistics import app
from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls
from manage_es import manager as es

manager = Manager(app)

@manager.command
def hello():
    """Hello world, manager style"""
    print "Hello, got those TPS reports ready?"

if __name__ == "__main__":
    manager.add_command("es", es)
    manager.add_command("urls", ShowUrls())
    manager.run()
