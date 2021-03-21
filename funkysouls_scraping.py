import re
from web_tor import driver
from credentials import funkysouls
from db import saving_users, count_is_null

# Готово:
# 99215 - Торрент трекеры I
# 99218 - Торрент трекеры II
# 164125 - Торрент трекеры III
# 272990 - Торрент трекеры IV

# Переходим на первую страницу темы
topic = 272990
driver.get(f"{funkysouls['url']}/t/{topic}")

count = 1
users = {}

# Определяем сколько страниц в теме
# Регулярным выражением '\d+' оставляем только цифры, переводим в int
pagination = driver.find_elements_by_xpath('//*[@id="content"]/section/header/div[1]/div[2]/span')[0].text
pagination = int(re.findall('\d+', pagination)[0])

# Проходим все страницы темы, сохраняя ники пользователей
# Каждый проход цикла увеличивает значение count на 1
# Выполняем цикл пока значение count меньше или равно pagination
while count <= pagination:
    driver.get(f"{funkysouls['url']}/t/{topic}_{count}")
    id_all = driver.find_elements_by_xpath('//*[@class="username"]/a')
    username = driver.find_elements_by_xpath('//*[@class="username"]')
    for x, y in zip(id_all, username):
        id = x.get_attribute("onclick")
        id = re.findall('\d+', id)[0]
        users[id] = y.text
    count += 1

table = 'funkysouls'

saving_users(table, users)

count_is_null(table)