import requests
from bs4 import BeautifulSoup
import csv
import json

HOST = 'https://stopgame.ru'
URL = 'https://stopgame.ru/review/new/izumitelno/p'
CSV = 'cards.csv'

def get_html_form_url(url, params=''):
    r = requests.get(url, params=params)
    return r


def get_content_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'item article-summary'})
    games = []
    # print(items)
    for item in items:
        games.append(
            {
                'title': item.find('div', class_='article-description').find('div', class_='caption caption-bold').get_text(strip=True),
                'link_img': item.find('a', class_='article-image image').find('img').get('src'),
                'date': item.find('div', class_='article-description').find('div', class_='info').find('span', class_='info-item timestamp').get_text().replace(u'\xa0', u' '),
                'link_article': HOST + item.find('div', class_='article-description').find('div', class_='caption caption-bold').find('a').get('href')
            }
        )
    return games

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название статьи', 'Ссылка на картинку', 'Дата публикации', 'Ссылка на статью'])
        for item in items:
            writer.writerow( [item['title'], item['link_img'], item['date'], item['link_article']])


def parser():
    pages = input('Укажите количество страниц для парсинга: ')
    pages = int(pages.strip())
    html = get_html_form_url(URL)
    if html.status_code == 200:
        cards = [get_content_from_html(get_html_form_url(URL + str(page)).text) for page in range(1, pages+1)]
        cards = []
        for page in range(1, pages+1):
            print(f'Парсим страницу - {page}')
            html = get_html_form_url(URL + str(page))
            cards.extend(get_content_from_html(html.text))
            # save_doc(cards, CSV)
        print('Парсинг закончился')
        return cards
    else:
        print('Error')


def save_into_csv():
    data = parser()
    save_doc(data, CSV)



def saev_into_json():
    value = parser()
    data = json.dumps(value,sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    with open('file.json', 'w', encoding='utf-8') as file:
        file.write(data)



