import time
import praw
import sqlite3
from credentials import user_agent, reddit, message_en


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

ignore = set()

subreddits = (
    # 'Invites', https://www.reddithelp.com/hc/en-us/articles/360049499032
    'OpenSignups',
    'seedboxes',
    'torrents',
    'trackers',
)

# Модераторы сабреддитов
for item in subreddits:
    for item in reddit.subreddit(item).moderator():
        ignore.add(item.name)

# С кем у нас была переписка
for item in reddit.inbox.sent(limit=None):
    ignore.add(item.dest.name)

users_db = sqlite3.connect('users.db')

exceptions_many = [
    'NOT_WHITELISTED_BY_USER_MESSAGE',
    'INVALID_USER'
]

while True:
    user_id = list(users_db.execute(f"select id from reddit where send is Null limit 1;"))[0][0]
    if user_id not in ignore:
        try:
            reddit.redditor(user_id).message('Private torrent trackers', message_en)
        except praw.exceptions.RedditAPIException as exception:
            print(user_id, exception)
            if exception.items[0].error_type in exceptions_many:
                pass
            elif exception.items[0].error_type == 'RATELIMIT':
                break
            else:
                raise
        users_db.execute(f"update reddit set send = 'Done' where id = '{user_id}';")
        users_db.commit()
        print(user_id, 'done')
        time.sleep(60)
    else:
        users_db.execute(f"update reddit set send = 'Ignore' where id = '{user_id}';")
        users_db.commit()
        print(user_id, 'ignore')
