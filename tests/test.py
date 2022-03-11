import urllib.request
from bs4 import BeautifulSoup

ifpa_url = 'https://belem.ifpa.edu.br/publicacoes'

page = urllib.request.urlopen(ifpa_url)

soup = BeautifulSoup(page, 'html5lib')

itens = soup.find_all('div', class_='span10 tileContent')

message = ''

for item in itens:
    item_link = str(item.find('a').get('href'))
    item = str(item)

    message += item.replace(item_link, f'{"https://belem.ifpa.edu.br"}{item_link}')

message_html = f'<html><body>{message}</body></html>'

print(message_html)

while True:
    pass