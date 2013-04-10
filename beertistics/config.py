import os

# Location of applicatoin root directory
BASE_DIR = os.path.normpath(os.path.dirname(__file__)+'/../')

# How long to cache data fetched from Untappd
CACHE_TIMEOUT = 1800

# Import all environment specific settings
from beertistics.env import *