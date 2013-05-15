from beertistics.views import general
from beertistics.views import login
from beertistics.views import api

from beertistics import app
if app.config["DEBUG"]:
    from beertistics.views import dev
