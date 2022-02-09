import re
from selenium.webdriver.common.by import By
import misc
from credentials import funkysouls

users = {}
topics = (
    # 99215,  # Торрент трекеры I
    # 99218,  # Торрент трекеры II
    # 164125,  # Торрент трекеры III
    272990,  # Торрент трекеры IV
    74739,  # Инвайты на FT / Invites
)

misc.count_is_null('funkysouls')
driver = misc.web_surfing(tor=True)

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

misc.saving_users('funkysouls', users)
misc.count_is_null('funkysouls')
