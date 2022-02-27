import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import misc
from credentials import pda, message_ru


# Переходим на страницу авторизации
driver = misc.web_surfing()
driver.get(f"{pda['url']}/forum/index.php?act=auth")

# Заполняем форму авторизации
driver.find_element(By.NAME, 'login').send_keys(pda['login'])
driver.find_element(By.NAME, 'password').send_keys(pda['password'])

# Ожидание для ввода капчи в ручную
time.sleep(20)
driver.find_element(By.CLASS_NAME, 'btn').click()

while True:
    user_id = misc.select_one_user_to_send('pda')
    driver.get(f"{pda['url']}/forum/index.php?act=qms&mid={user_id}")
    # Ожидание, чтобы загрузились все элементы страницы и для паузы между отправками
    time.sleep(10)
    # Заполнение формы отправки сообщения
    driver.find_element(By.NAME, 'title').send_keys("Частные торрент-трекеры")
    driver.find_element(By.NAME, 'message').send_keys(message_ru)
    driver.find_element(By.ID, 'create-thread-submit').click()
    time.sleep(10)
    # Прерываем отправку при "Не удалось создать новый диалог с пользователем. Попробуйте позднее."
    try:
        driver.find_element(By.CLASS_NAME, 'list-group-item.msgbox.error')
        print(user_id, 'break')
        break
    except NoSuchElementException:
        misc.successfully_sent('pda', user_id)

misc.count_is_null('pda')
