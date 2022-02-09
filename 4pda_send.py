import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import misc
from credentials import pda, message_ru


# Переходим на страницу авторизации
driver = misc.web_surfing()
driver.get(f"{pda['url']}/forum/index.php?act=auth")

# Для удобства сохраняем XPath формы авторизации
username = '//*[@id="auth"]/div[3]/input'
password = '//*[@id="auth"]/div[4]/input'
login = '//*[@id="auth"]/div[10]/input'

# Заполняем форму авторизации
driver.find_element(By.XPATH, username).send_keys(pda['login'])
driver.find_element(By.XPATH, password).send_keys(pda['password'])

# Ожидание для ввода капчи в ручную
time.sleep(20)
driver.find_element(By.XPATH, login).click()

# Для удобства сохраняем XPath формы отправки сообщения
title = '//*[@id="threads-bottom-form"]/div[3]/input'
body = '//*[@id="thread-msg"]'
button = '//*[@id="create-thread-submit"]'

error = '//*[@id="create-thread-messages"]/div'

while True:
    user_id = misc.select_one_user_to_send('pda')
    driver.get(f"{pda['url']}/forum/index.php?act=qms&mid={user_id}")
    # Ожидание, чтобы загрузились все элементы страницы и для паузы между отправками
    time.sleep(10)
    # Заполнение формы отправки сообщения
    driver.find_element(By.XPATH, title).send_keys("Частные торрент-трекеры")
    driver.find_element(By.XPATH, body).send_keys(message_ru)
    driver.find_element(By.XPATH, button).click()
    time.sleep(10)
    # Прерываем отправку при "Не удалось создать новый диалог с пользователем. Попробуйте позднее."
    try:
        driver.find_element(By.XPATH, error)
        print(user_id, 'break')
        break
    except NoSuchElementException:
        misc.successfully_sent('pda', user_id)

misc.count_is_null('pda')
