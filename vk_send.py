import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import misc
from credentials import vk


driver = misc.web_surfing()
driver.get(f"{vk['url']}")
time.sleep(5)
driver.find_element(By.ID, 'index_email').send_keys(vk['login'])
time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="index_login"]/div/form/button[1]/span/span').click()
time.sleep(5)
driver.find_element(By.NAME, 'password').send_keys(vk['password'])
time.sleep(5)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/form/div[2]/button/span[1]').click()
time.sleep(5)

send_text = (
    'Назад',
    'Отправить подарок'
)

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
            driver.find_element(By.ID, 'mail_box_editable').send_keys(misc.message_ru)
            time.sleep(5)
            driver.find_element(By.CLASS_NAME, 'FlatButton__content').click()
            time.sleep(5)
            if driver.find_element(By.ID, 'system_msg').text.startswith(system_msg) is True:
                print(user_id, "break")
                break
            else:
                misc.successfully_sent('vk', user_id)
                time.sleep(60)
        elif send.text.startswith(send_text) is True:
            misc.sending_error('vk', user_id)
    except NoSuchElementException:
        misc.sending_error('vk', user_id)

misc.count_is_null('vk')
