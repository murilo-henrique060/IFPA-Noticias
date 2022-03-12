from bs4 import BeautifulSoup

def decouple(html: BeautifulSoup):
    from decouple import config

    itens = html.find_all('div', class_='tile-collection')

    decouple_data = []

    base_url = config('url')

    for item in itens:
        i = item.find_all('a')
        decouple_data.append([])

        for a in i:
            decouple_data[-1].append([a.string.replace('\t','').replace('\n',''), base_url + a.get('href')])

    # for item in decouple_data:
    #     for i in item:
    #         print(f'\t{i[0]} - {i[1]}')
    #     print('\n', '='*20, '\n')

    return decouple_data

