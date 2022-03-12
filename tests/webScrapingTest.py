def urllibScraping(url: str): # using urllib to scrap when is running localy
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    return soup

print(urllibScraping('https://www.google.com'))