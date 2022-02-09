import re
from selenium.webdriver.common.by import By
import misc
from credentials import pda


users = {}
topics = (
    191879,  # Инвайты на закрытые ресурсы
)

misc.count_is_null('pda')

for topic in topics:
    driver = misc.web_surfing()
    driver.get(f"{pda['url']}/forum/index.php?showtopic={topic}")

    pages = int(re.findall('\d+', driver.find_element(By.CLASS_NAME, 'pagelink').text)[0]) * 20

    for page in range(0, pages, 20):
        driver.get(f"{pda['url']}/forum/index.php?showtopic={topic}&st={page}")
        all = driver.find_elements(By.XPATH, '//*[@class="normalname"]/a')
        for user in all:
            # Словарь {id: имя пользователя}
            users[re.findall('\d{2,}', user.get_attribute("href"))[0]] = user.text

misc.saving_users('pda', users)
misc.count_is_null('pda')

