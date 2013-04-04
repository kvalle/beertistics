from os.path import dirname, normpath

SECRET_KEY = 'dev_key'
DEBUG = True
BASE_DIR = normpath(dirname(__file__)+'/../')

## Must be changed according to where app is deployed
SERVER_NAME = '127.0.0.1:5000'

CACHE_TIMEOUT = 1800

UNTAPPD_CLIENT_ID = "C2B98311257562CC0BA3505452861DD8DF65DCC6"
UNTAPPD_CLIENT_SECRET = "9180BCBA0DFC55C76E125673F4D9F7D9E4A8B324"