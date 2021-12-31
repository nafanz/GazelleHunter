import re
from selenium.webdriver.common.by import By
from web import web
from db import saving_users, count_is_null
from credentials import pda

count = 0
users = {}

# Переходим на первую страницу темы
topic = 191879
driver = web('pass')
driver.get(f"{pda['url']}/forum/index.php?showtopic={topic}")

# Определяем сколько страниц в теме
# Регулярным выражением '\d+' оставляем только цифры, переводим в int * 20
pagination = driver.find_elements(By.XPATH, '//*[@id="page-jump-1"]')[0].text
pagination = int(re.findall('\d+', pagination)[0]) * 20

# Проходим все страницы темы, сохраняя ники пользователей
# Каждый проход цикла увеличивает значение count на 20
# Выполняем цикл пока значение count меньше или равно pagination
while count <= pagination:
    driver.get(f"{pda['url']}/forum/index.php?showtopic=191879&st={count}")
    id_all = driver.find_elements(By.XPATH, '//*[@class="normalname"]/a')
    username = driver.find_elements(By.XPATH, '//*[@class="normalname"]')
    for x, y in zip(id_all, username):
        id = x.get_attribute("href")
        id = re.findall('\d{2,}', id)[0]
        users[id] = y.text
    count += 20

table = 'pda'

saving_users(table, users)

count_is_null(table)