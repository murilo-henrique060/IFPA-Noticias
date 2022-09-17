from decouple import config
from datetime import strptime

# scraping url
URL = config("url")

# scrappingbot config
USER_NAME = config("userName")
API_KEY = config("apiKey")
API_END_POINT = config("apiEndPoint")
USE_CHROME = config("useChrome", cast=bool)
PREMIUM_PROXY = config("premiumProxy", cast=bool)
PROXY_COUNTRY = config("proxyCountry")
WAIT_FOR_NETWORK_REQUESTS = config("WaitForNetworkRequests", cast=bool)

# Email config
HOST = config("host")
PORT = config("port", cast=int)
USER = config("user")
PASSWORD = config("password")
TO = config("to")
TITLE = config("title")
TOPICS = config("topics")

# Alarm config
ALARM_TIME = strptime(config("alarmTime"), "%H:%M")

# Mode
MODE = config("mode")

# Database config
DATABASE_URL = config("databaseURL")