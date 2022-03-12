# this module is used to scrap the data from the website

def urllibScraping(url: str): # using urllib to scrap when is running localy
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def apiScraping(url: str): # using api to scrap when is running on server. api: scrapping-bot.io
    from decouple import config
    from json import dumps as json_dumps
    from requests import request
    from bs4 import BeautifulSoup

    username = config('user_name')
    apiKey = config('apiKey')

    apiEndPoint = config('apiEndPoint')

    options = {
        'useChrome': config('useChrome', cast=bool),
        'premiumProxy': config('premiumProxy', cast=bool),
        'proxyCountry': config('proxyCountry'),
        'waitForNetworkRequests': config('waitForNetworkRequests', cast=bool),
    }

    payload = json_dumps({"url":url,"options":options})
    headers = {
        'Content-Type': "application/json"
    }

    page = request("POST", apiEndPoint, data=payload, auth=(username,apiKey), headers=headers)

    soup = BeautifulSoup(page.text, 'html5lib')

    return soup