import json, smtplib, requests, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config
from bs4 import BeautifulSoup
from time import sleep

def urllibScraping(url: str): # using urllib to scrap when is running localy
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def apiScraping(url: str): # using api to scrap when is running on server. api: scrapping-bot.io
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

    soup = BeautifulSoup(page.text, 'html5lib')

    return soup

def scrapUrl(url: str, find_tag, find_class):
    soup = urllibScraping(url) if config('scraping_type') == 'urllib' else apiScraping(url)

    itens = soup.find_all(find_tag, class_=find_class)
    for item in itens:
        item_link = str(item.find('a').get('href'))

        for item_img in item.find_all('div', class_='tileImage'):
            item = str(item).replace(str(item_img), '')

    return soup.find(find_tag, class_=find_class)

def genMessage():
    url = config('url')
    soup = urllibScraping(url) if config('dev_mode') == 'urllib' else apiScraping(url)

    itens = soup.find_all('div', class_='span10 tileContent')

    message = ''

    for item in itens:
        item_link = str(item.find('a').get('href'))

        try:
            item_img = str(item.find('div', class_='tileImage'))

        except:
            pass

        else:
            item = str(item).replace(item_img, '')

        message += str(item).replace(item_link, f'{"https://belem.ifpa.edu.br"}{item_link}')

    message_html = f'<html><body>{message}</body></html>'

    return message_html

def sendEmail(message_html):
    host = config('host')
    port = config('port', cast=int)
    user = config('user')
    password = config('password')
    to = config('to')
    title = config('title')

    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(user, password)

    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = to
    email_msg['Subject'] = title

    email_msg.attach(MIMEText(message_html, 'html'))

    server.sendmail(email_msg['From'], to.split(', '), email_msg.as_string())

    server.quit()

def main():
    alarm_hour = config('alarm_hour', cast=int)
    alarm_minute = config('alarm_minute', cast=int)
    td = datetime.timedelta(hours = -3)
    tz = datetime.timezone(td)

    while True:
        tm = datetime.datetime.now(tz)

        print(tm.strftime('Hora atual - %H:%M'))

        if tm.hour == alarm_hour and tm.minute == alarm_minute:
            sendEmail(genMessage())
            print('Email enviado')

        sleep(60)

if __name__ == '__main__':
    main()