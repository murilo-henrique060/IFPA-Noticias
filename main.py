import requests
import json
from decouple import config
from bs4 import BeautifulSoup

url = config('url')
username = config('user_name')
apiKey = config('apiKey')

apiEndPoint = config('apiEndPoint')

options = {
    'useChrome': config('useChrome', cast=bool),
    'premiumProxy': config('premiumProxy', cast=bool),
    'proxyCountry': config('proxyCountry'),
    'waitForNetworkRequests': config('waitForNetworkRequests', cast=bool),
}

payload = json.dumps({"url":url,"options":options})
headers = {
    'Content-Type': "application/json"
}

page = requests.request("POST", apiEndPoint, data=payload, auth=(username,apiKey), headers=headers)

print(page.text)

soup = BeautifulSoup(page.text, 'html.parser')

itens = soup.find_all('div', class_='tileItem')

print(itens)

while True:
    pass