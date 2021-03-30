import time
from web import driver
from selenium.common.exceptions import NoSuchElementException
from db import select_one_user_to_send, successfully_sent, count_is_null
from credentials import pda, question, trackers

# Переходим на страницу авторизации
driver.get(f"{pda['url']}/forum/index.php?act=auth")

# Для удобства сохраняем XPath формы авторизации
username = '//*[@id="auth"]/div[3]/input'
password = '//*[@id="auth"]/div[4]/input'
login = '//*[@id="auth"]/div[10]/input'

# Заполняем форму авторизации
driver.find_element_by_xpath(username).send_keys(pda['login'])
driver.find_element_by_xpath(password).send_keys(pda['password'])

# Ожидание для ввода капчи в ручную
time.sleep(20)
driver.find_element_by_xpath(login).click()

# Для удобства сохраняем XPath формы отправки сообщения
title = '//*[@id="threads-bottom-form"]/div[3]/input'
body = '//*[@id="thread-msg"]'
button = '//*[@id="create-thread-submit"]'

error = '//*[@id="create-thread-messages"]/div'

# Подготавливаем полный текст сообщения
text = question['ru'] + '\n'.join(trackers)

# Указываем таблицу
table = 'pda'

while True:
    user_id = select_one_user_to_send(table)
    driver.get(f"{pda['url']}/forum/index.php?act=qms&mid={user_id}")
    # Ожидание, чтобы загрузились все элементы страницы и для паузы между отправками
    time.sleep(10)
    # Заполнение формы отправки сообщения
    driver.find_element_by_xpath(title).send_keys('Трекеры')
    driver.find_element_by_xpath(body).send_keys(text)
    driver.find_element_by_xpath(button).click()
    time.sleep(10)
    # Прерываем отправку при "Не удалось создать новый диалог с пользователем. Попробуйте позднее."
    try:
        driver.find_element_by_xpath(error)
        print(user_id, 'break')
        break
    except NoSuchElementException:
        successfully_sent(table, user_id)

count_is_null(table)