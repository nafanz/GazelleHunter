import requests
from lxml import html
from credentials import telegram, trackers


register_closed = (
    'Registration Closed',  # All
    '注册关闭'  # DICmusic
)

application_closed = (
    'Applications are currently closed.',  # AwesomeHD
    '你刚刚试图查看不存在的页面。'  # DICmusic
)

for item in trackers.values():
    if item is not None:
        register = requests.get(f'{item}/register.php')
        # Проверяем, что не было переадресации и ресурс доступен
        if register.url == f'{item}/register.php' and register.status_code == 200:
            parser = html.fromstring(register.text)
            text = parser.xpath('//title/text()')[0]
            # Если шаблоного текста нет - отправляем сообщение
            status = text.startswith(register_closed)
            if status is False:
                requests.post(
                    f"https://api.telegram.org/{telegram['bot_id']}:{telegram['bot_token']}/sendMessage",
                    json={
                        'chat_id': telegram['chat_id'],
                        'text': f'{register.url}\n{text}'
                    }
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
                    requests.post(
                        f"https://api.telegram.org/{telegram['bot_id']}:{telegram['bot_token']}/sendMessage",
                        json={
                            'chat_id': telegram['chat_id'],
                            'text': f'{application.url}\n{text}'
                        }
                    )
