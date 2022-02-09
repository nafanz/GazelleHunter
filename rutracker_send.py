import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import misc
from credentials import rutracker, question, trackers


# Переходим на страницу авторизации
driver = misc.web_surfing(tor=True)
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
    user_id = misc.select_one_user_to_send('rutracker')
    driver.get(f"{rutracker['url']}/forum/privmsg.php?mode=post&u={user_id}")
    # Заполнение формы отправки сообщения
    try:
        driver.find_element(By.ID, 'post-msg-subj').send_keys("Частные торрент-трекеры")
        driver.find_element(By.ID, 'post-textarea').send_keys(question['ru'] + '\n'.join(trackers))
        driver.find_element(By.ID, 'post-submit-btn').click()

        # Ваше сообщение было отправлено \ Вы превысили лимит количества исходящих сообщений (20)
        if driver.find_element(By.CLASS_NAME, 'mrg_16').text.startswith('Вы превысили лимит количества исходящих сообщений') is True:
            print(user_id, "break")  # На самом деле 10
            break
        else:
            misc.successfully_sent('rutracker', user_id)
    # Обрабатываем исключение если элемента нет
    # Возникает из-за того, что пользователю нельзя отправлять сообщения
    except NoSuchElementException:
        misc.sending_error('rutracker', user_id)
    # Ожидание
    time.sleep(60)

misc.count_is_null('rutracker')