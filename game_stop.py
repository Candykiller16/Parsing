import requests
from bs4 import BeautifulSoup as BS

with open('test.txt', 'w') as test:
    page = 1

    while True:
        r = requests.get("https://stopgame.ru/review/new/izumitelno/p" + str(page))
        html = BS(r.content, 'html.parser')
        items = html.select(".items > .article-summary")

        if len(items):
            for el in items:
                title = el.select('.prod__in > a')
                test.write(title[0].text + '\n')
            page += 1
        else:
          break