import json, smtplib, requests, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config
from bs4 import BeautifulSoup
from time import sleep

def getMessage():
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

    soup = BeautifulSoup(page.text, 'html5lib')

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

    while True:
        td = datetime.timedelta(hours=-3)
        tz = datetime.timezone(td)
        tm = datetime.datetime.now(tz)

        print(tm.strftime('Horário de Brasília - %H:%M'))

        if tm.hour == alarm_hour and tm.minute == alarm_minute:
            sendEmail(getMessage())
            print('Email enviado')
            break

        sleep(60)

if __name__ == '__main__':
    main()