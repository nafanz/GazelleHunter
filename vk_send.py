from db import select_one_user_to_send, successfully_sent, count_is_null
from credentials import vk, question, trackers
from selenium.webdriver.common.by import By
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
print(text)

while True:
    user_id = select_one_user_to_send('vk')
    driver.get(f"{vk['url']}/im?sel={user_id}")
    time.sleep(10)
    driver.find_element(By.CLASS_NAME, 'im_editable.im-chat-input--text._im_text').send_keys(text)
    time.sleep(10)
    driver.find_element(By.CLASS_NAME, 'im-send-btn.im-chat-input--send._im_send.im-send-btn_send').click()
    time.sleep(10)
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