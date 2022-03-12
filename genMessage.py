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
