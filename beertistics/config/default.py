DEBUG = True

# Location of applicatoin root directory
import os
BASE_DIR = os.path.normpath(os.path.dirname(__file__)+'/../../')

# How long to cache data fetched from Untappd (in seconds)
CACHE_TIMEOUT = 1800

# Stub signin and data retrieval from Untappd
UNTAPPD_STUB = True

# Key used for signing sessions
SECRET_KEY = "dev_key"

## Must be changed according to where app is deployed
SERVER_NAME = '127.0.0.1:5000'
