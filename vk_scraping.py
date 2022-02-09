import re
from selenium.webdriver.common.by import By
import vk as api_key
import sqlite3
import misc
from credentials import vk


# Переходим на страницу авторизации
driver = misc.web_surfing()
driver.get(f"https://oauth.vk.com/authorize?client_id={vk['application']}]&response_type=token")

# Заполняем форму авторизации
driver.find_element(By.NAME, 'email').send_keys(f"{vk['login']}")
driver.find_element(By.NAME, 'pass').send_keys(f"{vk['password']}")
driver.find_element(By.ID, 'install_allow').click()

token = re.findall('[a-z0-9]{10,}', driver.current_url)[0]

driver.quit()

api = api_key.Api(token)

users = set()

groups = [
    'club85955762',
    'invitesmag',
    'flac_music',
    'jpopsuki',
    'btinvite',
    'club3111532',
    'deepbassnine',
    'club9680876'
]

for item in [group for group in api.get_groups(groups)]:
    for i in item.get_members():
        if i.can_write_private_message is True and i.is_friend is False:
            users.add(
                    (
                        i.id,
                        i.first_name,
                        i.last_name
                    )
                )

table = 'vk'
users_db = sqlite3.connect('users.db')

users_db.executemany(f"""
    INSERT OR IGNORE INTO {table} (
        id,
        first_name,
        last_name        
        ) 
        values(?, ?, ?)
""", users)

users_db.commit()

misc.count_is_null(table)