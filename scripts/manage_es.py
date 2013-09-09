#!/usr/bin/env python

import time
import json
import os
import subprocess
from functools import wraps
from socket import error as SocketError
from os.path import join, dirname, realpath, isfile

from flask.ext.script import Manager, prompt_bool
from beertistics import app, search

# Set current working directory to beertistics root folder
os.chdir(join(dirname(realpath(__file__)), ".."))

#
# Helper functions
#

def es_is_running():
    try:
        return bool(search.status())
    except SocketError, e:
        return False

def ensure_es_running(fn):
    """Wrapper for catching ES connection exception"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if es_is_running():
            return fn(*args, **kwargs)
        else:
            return 'ES don\'t appear to be running...'
    return wrapper

#
# Commands
#

manager = Manager(app, \
    with_default_commands=False, \
    usage="Perform operations on Elastic Search")

@manager.command
@ensure_es_running
def clear_index():
    """Clear all data from Elastic Search indexes"""
    if prompt_bool("Really clean index?"):
        print json.dumps(search.clear_index(), indent=4)
    else:
        print

@manager.command
@ensure_es_running
def status():
    """Display status info for Elastic Search"""
    print json.dumps(search.status(), indent=4)

@manager.command
def start():
    """Start an ES server instance"""
    if es_is_running():
        return "ES is already running..."
    start_es = "es/bin/elasticsearch -p es.pid"
    subprocess.Popen(start_es, shell=True)
    while not isfile("es.pid"):
        time.sleep(0.1)
    pid = subprocess.check_output(["cat", "es.pid"])
    return "ES is starting with PID %s" % pid

@manager.command
def stop():
    """Stop the currently running ES instance"""
    if not es_is_running():
        return "ES don't appear to be running..."
    if not isfile("es.pid"):
        return "ES is running, but I don't know the PID"
    pid = subprocess.check_output(["cat", "es.pid"])
    return_code = subprocess.call(["kill", pid])
    if return_code != 0:
        return "Unable to stop ES :("
    else:
        return "ES stopped."

@manager.command
def restart():
    """Restart ES (or simply start one if none are running)"""
    if es_is_running():
        stop()
    start()
    return "ES is restarting..."