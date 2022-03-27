import time
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import misc
import credentials


for mail in credentials.mail_ru.items():
    driver = misc.web_surfing()
    driver.get('https://account.mail.ru')
    time.sleep(5)
    driver.find_element(By.NAME, 'username').send_keys(mail[0])
    driver.find_element(By.XPATH, '//span[text()="Ввести пароль"]').click()
    time.sleep(5)
    driver.find_element(By.NAME, 'password').send_keys(mail[1])
    driver.find_element(By.XPATH, '//span[text()="Войти"]').click()
    time.sleep(60)
    driver.quit()

for mail in credentials.cock_li.items():
    driver = misc.web_surfing(tor=True)
    driver.get('https://mail.cock.li')
    time.sleep(5)
    driver.find_element(By.NAME, '_user').send_keys(mail[0])
    driver.find_element(By.NAME, '_pass').send_keys(mail[1])
    driver.find_element(By.ID, 'rcmloginsubmit').click()
    time.sleep(60)
    driver.quit()

spreadsheet = requests.get('https://nafanz.github.io/spreadsheet.json').json()['spreadsheet']

for item in spreadsheet:
    start = item['Name'].split('<a href="')[1]
    end = start.split('">')[0]
    print(end)
    driver = misc.web_surfing(tor=True)
    try:
        driver.get(end)
        time.sleep(30)
        driver.quit()
    except WebDriverException:
        driver.quit()
