user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

telegram = {
    'bot_id': 'XXX',
    'bot_token': 'XXX',
    'chat_id': 0
}

vk = {
    'id': 0,
    'login': 'XXX',
    'password': 'XXX',
    'application': 'XXX'
}

reddit = {
    'login': 'XXX',
    'password': 'XXX',
    'client_id': 'XXX',
    'client_secret': 'XXX'
}

rutracker = {
    'login': 'XXX',
    'password': 'XXX',
    'url': 'https://rutracker.org'
}

funkysouls = {
    'login': 'XXX',
    'password': 'XXX',
    'url': 'https://forum.funkysouls.org'
}

pda = {
    'login': 'XXX',
    'password': 'XXX',
    'url': 'https://4pda.to'
}

question = {
    'ru': 'Привет. Ты являешься участником какого-то из этих трекеров?\n\n',
    'en': 'Hey. Are you a member of any of these trackers?\n\n'
}

trackers = {
    'BrasilTracker': 'https://brasiltracker.org',
    'Anthelion': 'https://anthelion.me',
    'BroadcasTheNet': 'https://broadcasthe.net',
    'DICMusic': 'https://dicmusic.club',
    'GreatPosterWall': 'https://greatposterwall.com',
    'HeBits': 'https://hebits.net',
    'Materialize': 'https://materialize.is',
    'MorethanTV': 'https://www.morethantv.me',
    'PixelCove': 'https://www.pixelcove.me'
}

message_ru = question['ru'] + '\n'.join(trackers)
message_en = question['en'] + '\n\n'.join(trackers)  # Reddit
