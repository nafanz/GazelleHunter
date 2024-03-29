import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


users_db = sqlite3.connect('users.db')


def web_surfing(tor=False):
    if tor is True:
        options = Options()
        # https://hideip.me/ru/proxy/socks5list
        # Использование прокси, Tor Browser должен быть запущен
        options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
        # options.add_argument("headless")
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options
        )
    else:
        driver = webdriver.Chrome(
            ChromeDriverManager().install()
        )

    return driver


def saving_users(table, users):
    users_db.executemany(f"insert or ignore into {table} (id, username) values(?, ?)", users.items())
    users_db.commit()


def select_one_user_to_send(table):
    user_id = list(users_db.execute(f"select id from {table} where send is Null limit 1;"))[0][0]

    return user_id


def successfully_sent(table, user_id):
    users_db.execute(f"update {table} set send = 'Done' where id = {user_id};")
    users_db.commit()

    print(user_id, 'done')


def sending_error(table, user_id):
    users_db.execute(f"update {table} set send = 'Ignore' where id = {user_id};")
    users_db.commit()

    print(user_id, 'ignore')


def count_is_null(table):
    count = users_db.execute(f"select count(*) from {table} where send is Null;")

    print('Осталось:', count.fetchone()[0])

question = {
    'ru': 'Привет. Ты являешься участником какого-то из этих трекеров?\n\n',
    'en': 'Hey. Are you a member of any of these trackers?\n\n\n'
}

trackers = {
    'BroadcasTheNet': 'https://broadcasthe.net',
    'D3si': 'https://d3si.net',
    'DICMusic': 'https://dicmusic.club',
    'Materialize': 'https://materialize.is'
}

message_ru = question['ru'] + '\n'.join(trackers)
message_en = question['en'] + '\n\n'.join(trackers)  # Reddit