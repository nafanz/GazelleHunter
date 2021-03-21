import requests
from lxml import html
from vk_messages import MessagesAPI
from vk_messages.utils import get_random
import credentials

messages = MessagesAPI(
    login=credentials.vk['login'],
    password=credentials.vk['password'],
    cookies_save_path=''
)

register_closed = (
    'Registration Closed',  # All
    '注册关闭'  # DICmusic
)

application_closed = (
    'Applications are currently closed.',  # AwesomeHD
    '你刚刚试图查看不存在的页面。'  # DICmusic
)

for item in credentials.trackers.values():
    if item is not None:
        register = requests.get(f'{item}/register.php')
        # Проверяем, что не было переадресации и ресурс доступен
        if register.url == f'{item}/register.php' and register.status_code == 200:
            parser = html.fromstring(register.text)
            text = parser.xpath('//title/text()')[0]
            # Если шаблоного текста нет - отправляем сообщение
            status = text.startswith(register_closed)
            if status is False:
                messages.method(
                    'messages.send',
                    user_id=credentials.vk['id'],
                    message=f'{register.url}\n{text}',
                    random_id=get_random()
                )
        application = requests.get(f'{item}/application.php')
        if application.url == f'{item}/application.php' and application.status_code == 200:
            parser = html.fromstring(application.text)
            test = parser.xpath('//div/p/text()')
            # Так как BroadcasTheNet другая разметка страницы, мы его пока выкидываем
            if test:
                text = text[0]
                status = text.startswith(application_closed)
                if status is False:
                    messages.method(
                        'messages.send',
                        user_id=credentials.vk['id'],
                        message=f'{application.url}\n{text}',
                        random_id=get_random()
                    )
