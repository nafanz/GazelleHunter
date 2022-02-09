import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import misc
from credentials import vk, message_ru


driver = misc.web_surfing()
driver.get(f"{vk['url']}")
driver.find_element(By.ID, 'index_email').send_keys(f"{vk['login']}")
driver.find_element(By.ID, 'index_pass').send_keys(f"{vk['password']}")
driver.find_element(By.ID, 'index_login_button').click()
time.sleep(10)

system_msg = 'Сообщение не может быть отправлено, так как вы разослали слишком много сообщений за последнее время'

while True:
    user_id = misc.select_one_user_to_send('vk')
    driver.get(f"{vk['url']}/id{user_id}")
    time.sleep(5)
    try:
        send = driver.find_element(By.CLASS_NAME, 'FlatButton__content')
        if send.text.startswith('Написать сообщение') is True:
            send.click()
            time.sleep(5)
            driver.find_element(By.ID, 'mail_box_editable').send_keys(message_ru)
            time.sleep(5)
            driver.find_element(By.CLASS_NAME, 'FlatButton__content').click()
            time.sleep(5)
            if driver.find_element(By.ID, 'system_msg').text.startswith(system_msg) is True:
                print(user_id, "break")
                break
            else:
                misc.successfully_sent('vk', user_id)
        elif send.text.startswith('Отправить подарок') is True:
            misc.sending_error('vk', user_id)
    except NoSuchElementException:
        misc.sending_error('vk', user_id)

misc.count_is_null('vk')
