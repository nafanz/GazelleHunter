# https://praw.readthedocs.io/en/latest/
# https://praw.readthedocs.io/en/latest/getting_started/logging.html

import time
import praw
from credentials import user_agent, reddit, question, trackers

# client_id и client_secret взял из предварительно созданного приложения https://www.reddit.com/prefs/apps/
# user_agent взял из браузера
# username и password нужны только для публикации, для просмотра их можно не указывать
reddit = praw.Reddit(
    client_id=reddit['client_id'],
    client_secret=reddit['client_secret'],
    user_agent=user_agent,
    username=reddit['login'],
    password=reddit['password']
)

# Подготавливаем полный текст сообщения
text = question['en'] + '\n\n'.join(trackers)

comments = []
nickname = set()
ignore = set()

subreddits = (
    'seedboxes',
    'trackers',
    'torrents'
)

# https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html?highlight=moderator#praw.models.Subreddit.moderator
for item in subreddits:
    for item in reddit.subreddit(item).moderator():
        ignore.add(item.name)

# Формируем список пользователей с кем у нас была переписка
# https://praw.readthedocs.io/en/latest/code_overview/reddit/inbox.html?highlight=sent#praw.models.Inbox.sent
for item in reddit.inbox.sent(limit=None):
    ignore.add(item.dest.name)

# В каждом сабреддите отбираем N (limit=) новых записей
# Сохраняем имя автора и id комментария
for item in subreddits:
    for item in reddit.subreddit(item).new(limit=5):
        if item.author is None:
            pass
        else:
            comments.append(item.id)
            nickname.add(item.author.name)

# Получаем из комментария имя пользователя
for item in comments:
    submission = reddit.submission(id=item)
    submission.comments.replace_more(limit=None)
    for item in submission.comments.list():
        if item.author is None:
            pass
        else:
            nickname.add(item.author.name)

# После каждого отправленного сообщение выводим 'nickname + send' и засыпаем
for item in nickname:
    if item not in ignore:
        reddit.redditor(item).message('Trackers', text)
        print(item, 'send')
        time.sleep(30)