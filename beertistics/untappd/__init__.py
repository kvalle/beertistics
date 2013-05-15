from beertistics import app

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

if app.config["UNTAPPD_STUB"]:
    from beertistics.untappd.stub import *
else:
    from beertistics.untappd.impl import *
