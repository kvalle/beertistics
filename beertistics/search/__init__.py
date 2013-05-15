from beertistics import app

if app.config["SEARCH_STUB"]:
    from beertistics.search.stub import *
else:
    from beertistics.search.impl import *
