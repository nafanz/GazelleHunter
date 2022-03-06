import time
from selenium.webdriver.common.by import By
import misc
import credentials


for mail in credentials.mails.items():
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