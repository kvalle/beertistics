import sys, os

# Location of applicatoin root directory
BASE_DIR = os.path.normpath(os.path.dirname(__file__)+'/../')

# How long to cache data fetched from Untappd (in seconds)
CACHE_TIMEOUT = 1800

# Add system and environment specific configuration
sys.path.append(BASE_DIR + '/conf/')
from system_env import *