import re
from selenium.webdriver.common.by import By
from web import web
from credentials import funkysouls
from db import saving_users, count_is_null

users = {}
topics = (
    # 99215,  # Торрент трекеры I
    # 99218,  # Торрент трекеры II
    # 164125,  # Торрент трекеры III
    272990,  # Торрент трекеры IV
    74739,  # Инвайты на FT / Invites
)

count_is_null('funkysouls')
driver = web('tor')

for topic in topics:
    driver.get(f"{funkysouls['url']}/t/{topic}")

    pages = int(driver.find_element(By.CLASS_NAME, 'total').text[1:-1])

    for page in range(1, pages+1):
        driver.get(f"{funkysouls['url']}/t/{topic}_{page}")
        # Все пользователи на странице
        all = driver.find_elements(By.CSS_SELECTOR, 'li.username a')
        for user in all:
            # Словарь {id: имя пользователя}
            users[re.findall('\d+', user.get_attribute("onclick"))[0]] = user.text

saving_users('funkysouls', users)
count_is_null('funkysouls')
