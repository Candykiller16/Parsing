import requests
from bs4 import BeautifulSoup

URL = "https://home.1k.by/kitchen-coffeemakers/"


def get_html_form_url(url, params=''):
    r = requests.get(url, params=params)
    return r


def get_content_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'prod'})
    makers = []
    for item in items:
        makers.append(
            item.find('div', class_='prod__in').find('header', class_='prod__head').find('a').get_text(strip=True))
    return makers


def parser():
    pages = input('Укажите количество страниц для парсинга: ')
    pages = int(pages.strip())
    html = get_html_form_url(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, pages + 1):
            print(f'Парсим страницу - {page}')
            html = get_html_form_url(URL + 'page' + str(page))
            cards.extend(get_content_from_html(html.text))
        print('Парсинг закончился')
        return cards
    else:
        print('Error')


def save_in_txt():
    value = parser()
    with open('coffee-makers.txt', 'w', encoding='utf-8') as file:
        for item in value:
            file.write(item + '\n')


save_in_txt()
