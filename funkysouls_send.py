import time
from web import web
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from db import select_one_user_to_send, successfully_sent, count_is_null
from credentials import funkysouls, question, trackers


# Заполняем форму авторизации
driver = web('tor')
driver.get(f"{funkysouls['url']}/login")
driver.find_element(By.ID, 'username').send_keys(f"{funkysouls['login']}")
driver.find_element(By.ID, 'password').send_keys(f"{funkysouls['password']}")
driver.find_element(By.CSS_SELECTOR, '.controls > button:nth-child(1)').click()

while True:
    user_id = select_one_user_to_send('funkysouls')
    driver.get(f"{funkysouls['url']}/u/{user_id}/pm")
    # Заполнение формы отправки сообщения
    try:
        driver.find_element(By.NAME, 'msg_title').send_keys('Частные торрент-трекеры')
        driver.find_element(By.ID, 'answer_form').send_keys(question['ru'] + '\n'.join(trackers))
        driver.find_element(By.ID, 'add_tracking').click()
        driver.find_element(By.NAME, 'submit').click()
        successfully_sent('funkysouls', user_id)
        count_is_null('funkysouls')
        # Ожидание
        time.sleep(10)
    # Закрытие попапа о новом сообщении, который прерывает отправку
    except ElementNotInteractableException:
        driver.find_element(By.CLASS_NAME, 'close').click()
