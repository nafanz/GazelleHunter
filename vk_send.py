from vk_messages import MessagesAPI
from vk_messages.utils import get_random
from db import select_one_user_to_send, successfully_sent, count_is_null
from credentials import vk, question, trackers

messages = MessagesAPI(
    login=vk['login'],
    password=vk['password'],
    cookies_save_path=''
)

# Подготавливаем полный текст сообщения
text = question['ru'] + '\n'.join(trackers)

# Указываем таблицу
table = 'vk'

while True:
    user_id = select_one_user_to_send(table)
    try:
        messages.method(
            'messages.send',
            user_id=user_id,
            message=text,
            random_id=get_random()
        )
        successfully_sent(table, user_id)
    except:
        print(user_id, 'break')
        break

count_is_null(table)