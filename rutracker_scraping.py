import requests
from lxml import html
import sqlite3
from credentials import rutracker
from db import count_is_null

topic = 5860392
r = requests.get(f"{rutracker['url']}/forum/viewtopic.php?t={topic}")

# Преобразуем данные для парсинга
parser = html.fromstring(r.text)

# Получаем колличество страниц в теме
pagination = parser.xpath('//a[@class="pg"]/@href')

pg = set()

# Обрезаем list оставляя только номера страниц
# Так как пагинация есть сверху и снизу страницы мы оставляем только уникальные значения
for item in pagination:
    start = item.split(f'viewtopic.php?t={topic}&start=')
    for i in start:
        if i is not '':
            pg.add(i)

# Сохраняем значение последней страницы в теме
# Конвертируем str в int, нужно для сравнения с count
pagination_max = int(max(pg, key=lambda x:int(x)))
count = 0

users = {}

# Проходим все страницы темы, сохраняя ники пользователей
# Каждый проход цикла увеличивает значение count на 30
# Выполняем цикл пока значение count меньше или равно pagination
while count <= pagination_max:
    r = requests.get(f"{rutracker['url']}/forum/viewtopic.php?t={topic}&start={count}")
    parser = html.fromstring(r.text)
    id_all = parser.xpath('//a[2][@class="txtb"]/@href')
    username = parser.xpath('//tbody/tr[1]/td[1]/p[1]/text()')
    for x, y in zip(username, id_all):
        y = y.split('privmsg.php?mode=post&u=')[1]
        users[y] = x
    count += 30

table = 'rutracker'
users_db = sqlite3.connect('users.db')

users_db.executemany(f"""
    INSERT OR IGNORE INTO {table} (
        id,
        username  
        ) 
        values(?, ?)
""", users.items())

users_db.commit()

count_is_null(table)
