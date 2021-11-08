import time
from selenium.common.exceptions import NoSuchElementException
from web_def import driver, authorization
from db import select_one_user_to_send, successfully_sent, sending_error, count_is_null
from credentials import rutracker, question, trackers

# Переходим на страницу авторизации
driver.get(f"{rutracker['url']}/forum/login.php")

# Для удобства сохраняем XPath формы авторизации
username = '//*[@id="login-form-full"]/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/input'
password = '//*[@id="login-form-full"]/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]/input'
login = '//*[@id="login-form-full"]/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td/input'

# Заполняем форму авторизации
authorization(rutracker, username, password, login)

# Для удобства сохраняем XPath формы отправки сообщения
title = '//*[@id="post-msg-subj"]'
body = '//*[@id="post-textarea"]'
button = '//*[@id="post-submit-btn"]'

# Ваше сообщение было отправлено \ Вы превысили лимит количества исходящих сообщений (20)
status = '//*[@id="main_content_wrap"]/table/tbody/tr[2]/td/div[1]'

# Подготавливаем полный текст сообщения
text = question['ru'] + '\n'.join(trackers)

# Указываем таблицу
table = 'rutracker'

# Отправляем сообщения в цикле, заполняем send в базе
while True:
    user_id = select_one_user_to_send(table)
    driver.get(f"{rutracker['url']}/forum/privmsg.php?mode=post&u={user_id}")
    # Заполнение формы отправки сообщения
    try:
        driver.find_element_by_xpath(title).send_keys("Трекеры")
        driver.find_element_by_xpath(body).send_keys(text)
        driver.find_element_by_xpath(button).click()

        check_status = driver.find_element_by_xpath(status).text
        check_status = check_status.startswith('Вы превысили лимит количества исходящих сообщений (20)')
        if check_status is True:
            print(user_id, "break")
            break
        else:
            successfully_sent(table, user_id)
    # Обрабатываем исключение если элемента нет
    # Возникает из-за того, что пользователю нельзя отправлять сообщения
    except NoSuchElementException:
        sending_error(table, user_id)
    # Ожидание
    time.sleep(60)

count_is_null(table)