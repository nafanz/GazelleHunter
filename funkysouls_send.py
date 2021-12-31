import time
from web import web, authorization
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from db import select_one_user_to_send, successfully_sent, count_is_null
from credentials import funkysouls, question, trackers


# Переходим на страницу авторизации
driver = web('tor')
driver.get(f"{funkysouls['url']}/login")

# Для удобства сохраняем XPath формы авторизации
username = '//*[@id="username"]'
password = '//*[@id="password"]'
login = '//*[@id="login-form"]/div/button'

# Заполняем форму авторизации
authorization(driver, funkysouls, username, password, login)

# Для удобства сохраняем XPath формы отправки сообщения
title = '//*[@id="content"]/div[3]/div/form/div[2]/fieldset/input'
body = '//*[@id="answer_form"]'
checkbox = '//*[@id="add_tracking"]'
button = '//*[@id="answer"]/div[2]/div[3]/input[1]'
pop_up = '/html/body/div[2]/div[1]/span'

# Подготавливаем полный текст сообщения
text = question['ru'] + '\n'.join(trackers)

# Указываем таблицу
table = 'funkysouls'

while True:
    user_id = select_one_user_to_send(table)
    driver.get(f"{funkysouls['url']}/u/{user_id}/pm")
    # Заполнение формы отправки сообщения
    try:
        driver.find_element(By.XPATH, title).send_keys('Трекеры')
        driver.find_element(By.XPATH, body).send_keys(text)
        driver.find_element(By.XPATH, checkbox).click()
        driver.find_element(By.XPATH, button).click()
        successfully_sent(table, user_id)
        count_is_null(table)
        # Ожидание
        time.sleep(10)
    # Закрытие попапа о новом сообщении, который прерывает отправку
    except ElementNotInteractableException:
        driver.find_element(By.XPATH, pop_up).click()