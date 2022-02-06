from db import select_one_user_to_send, successfully_sent, count_is_null
from credentials import vk, question, trackers
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from web import web
import time


driver = web('pass')
driver.get(f"{vk['url']}")
driver.find_element(By.ID, 'index_email').send_keys(f"{vk['login']}")
driver.find_element(By.ID, 'index_pass').send_keys(f"{vk['password']}")
driver.find_element(By.ID, 'index_login_button').click()
time.sleep(10)

# Подготавливаем полный текст сообщения
text = question['ru'] + '\n'.join(trackers)

system_msg = 'Сообщение не может быть отправлено, так как вы разослали слишком много сообщений за последнее время'

while True:
    user_id = select_one_user_to_send('vk')
    driver.get(f"{vk['url']}/id{user_id}")
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'FlatButton__content').click()
    time.sleep(5)
    driver.find_element(By.ID, 'mail_box_editable').send_keys(text)
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'FlatButton__content').click()
    time.sleep(5)
    try:
        if driver.find_element(By.ID, 'system_msg').text.startswith(system_msg) is True:
            print(user_id, "break")
            break
    except NoSuchElementException:
        successfully_sent('vk', user_id)

# count_is_null('vk')
#
# while True:
#     user_id = select_one_user_to_send('vk')
#     try:
#         messages.method(
#             'messages.send',
#             user_id=user_id,
#             message=text,
#             random_id=get_random()
#         )
#         successfully_sent('vk', user_id)
#     except:
#         print(user_id, 'break')
#         break