import re
from selenium.webdriver.common.by import By
import misc
from credentials import rutracker


driver = misc.web_surfing('pass')
driver.get(f"{rutracker['url']}/forum/login.php")

driver.find_element(
    By.XPATH,
    './html/body/div[4]/div[1]/div[2]/table/tbody/tr/td/div/form/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/input'
).send_keys(f"{rutracker['login']}")

driver.find_element(
    By.XPATH,
    '/html/body/div[4]/div[1]/div[2]/table/tbody/tr/td/div/form/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]/input'
).send_keys(f"{rutracker['password']}")

driver.find_element(By.CLASS_NAME, 'bold.long').click()

topics = {}
keys = (
    'Вопросы по контенту закрытых трекеров',
    'Зарубежные аналоги RuTracker',
    'Обсуждение закрытых трекеров',
    'Предложения инвайтов на закрытые трекеры',
    'Просьбы инвайтов на закрытые трекеры',
    'Скрипты для торрент трекеров',
    'Сообщения об открытой регистрации на трекерах'
)

for key in keys:
    driver.find_element(By.ID, 'search-text').clear()
    driver.find_element(By.ID, 'search-text').send_keys(key)
    driver.find_element(By.ID, 'search-menu').send_keys(' все темы')
    driver.find_element(By.ID, 'search-submit').click()

    viewtopics = driver.find_elements(By.CLASS_NAME, 'topictitle.ts-text')

    for topic in viewtopics:
        topics[re.findall('\d+', topic.get_attribute("href"))[0]] = topic.text

for x in sorted(topics.items()):
    print(x[0],',  #', x[1])
