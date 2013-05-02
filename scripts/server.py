#!/usr/bin/env python

import sys
import os.path

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir + "/..")

if __name__=='__main__':
    from beertistics import app
    app.run()
