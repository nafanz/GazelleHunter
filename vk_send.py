from db import select_one_user_to_send, successfully_sent, count_is_null
from credentials import vk, question, trackers
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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