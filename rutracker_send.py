import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from web import web
from db import select_one_user_to_send, successfully_sent, sending_error, count_is_null
from credentials import rutracker, question, trackers


# Переходим на страницу авторизации
driver = web('tor')
driver.get(f"{rutracker['url']}/forum/login.php")

# Для удобства сохраняем XPath формы авторизации
username = '//*[@id="login-form-full"]/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/input'
password = '//*[@id="login-form-full"]/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]/input'

# Заполняем форму авторизации
driver.find_element(By.XPATH, username).send_keys(f"{rutracker['login']}")
driver.find_element(By.XPATH, password).send_keys(f"{rutracker['password']}")
driver.find_element(By.CLASS_NAME, 'bold.long').click()

# Отправляем сообщения в цикле, заполняем send в базе
while True:
    user_id = select_one_user_to_send('rutracker')
    driver.get(f"{rutracker['url']}/forum/privmsg.php?mode=post&u={user_id}")
    # Заполнение формы отправки сообщения
    try:
        driver.find_element(By.ID, 'post-msg-subj').send_keys("Частные торрент-трекеры")
        driver.find_element(By.ID, 'post-textarea').send_keys(question['ru'] + '\n'.join(trackers))
        driver.find_element(By.ID, 'post-submit-btn').click()

        # Ваше сообщение было отправлено \ Вы превысили лимит количества исходящих сообщений (20)
        if driver.find_element(By.CLASS_NAME, 'mrg_16').text.startswith('Вы превысили лимит количества исходящих сообщений (20)') is True:
            print(user_id, "break")  # На самом деле 10
            break
        else:
            successfully_sent('rutracker', user_id)
    # Обрабатываем исключение если элемента нет
    # Возникает из-за того, что пользователю нельзя отправлять сообщения
    except NoSuchElementException:
        sending_error('rutracker', user_id)
    # Ожидание
    time.sleep(60)

count_is_null('rutracker')