import time
import praw
import sqlite3
from credentials import user_agent, reddit


reddit = praw.Reddit(
    client_id=reddit['client_id'],
    client_secret=reddit['client_secret'],
    user_agent=user_agent,
    username=reddit['login'],
    password=reddit['password']
)

comments = []
users = set()

subreddits = (
    # 'Invites', Done
    'OpenSignups',
    # 'seedboxes',
    # 'torrents',
    # 'trackers',
)

# В каждом сабреддите отбираем N (limit=) новых записей
# Сохраняем имя автора и id комментария
for item in subreddits:
    for item in reddit.subreddit(item).new(limit=None):
        if item.author is None:
            pass
        else:
            comments.append(item.id)
            users.add(item.author.name)

# Получаем из комментария имя пользователя
for item in comments:
    submission = reddit.submission(id=item)
    submission.comments.replace_more(limit=None)
    for item in submission.comments.list():
        if item.author is None:
            pass
        else:
            users.add(item.author.name)

users_db = sqlite3.connect('users.db')

for user in users:
    users_db.execute(f"insert or ignore into reddit (user) values('{user}')")
    users_db.commit()