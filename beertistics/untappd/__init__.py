from beertistics import app

if app.config["UNTAPPD_STUB"]:
    from beertistics.untappd.untappd_stub import *
else:
    from beertistics.untappd.untappd_impl import *