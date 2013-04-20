#!/usr/bin/env python

import os
os.environ["BEERTISTICS_CONFIG"] = "production"

if __name__=='__main__':
    from beertistics import app
    app.run()
