import smtplib, datetime
from decouple import config
from time import sleep

from scraping import *
from sendEmail import *

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
    soup = urllibScraping(url) if config('scraping_mode') == 'urllib' else apiScraping(url)

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

def prodMode():
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

def devMode():
    from os import exit as os_exit
    message = genMessage()
    print(message)
    sendEmail(message)
    input('Press any key to do exit...')
    os_exit(0)

def main():
    if config('dev_mode') == 'dev':
        devMode()
    else:
        prodMode()

if __name__ == '__main__':
    main()