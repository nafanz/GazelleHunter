import re
from selenium.webdriver.common.by import By
from web import web
from credentials import funkysouls
from db import saving_users, count_is_null

# Готово:
# 99215 - Торрент трекеры I
# 99218 - Торрент трекеры II
# 164125 - Торрент трекеры III
# 272990 - Торрент трекеры IV

# Переходим на первую страницу темы
topic = 272990

driver = web('tor')
driver.get(f"{funkysouls['url']}/t/{topic}")

# Определяем количество страниц в теме
pagination = int(driver.find_element(By.CSS_SELECTOR, 'div.pagination:nth-child(3) > span:nth-child(2)').text[1:-1])

users = {}

for page in range(1, pagination+1):
    driver.get(f"{funkysouls['url']}/t/{topic}_{page}")
    # Все пользователи на странице
    all = driver.find_elements(By.CSS_SELECTOR, 'li.username a')
    for user in all:
        # Словарь {id: имя пользователя}
        users[re.findall('\d+', user.get_attribute("onclick"))[0]] = user.text

table = 'funkysouls'

saving_users(table, users)

count_is_null(table)