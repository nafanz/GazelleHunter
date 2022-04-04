import math
import requests


repos = 'HDVinnie/Private-Trackers-Spreadsheet'
per_page = 100
page = math.ceil(311/per_page)

email = set()

for x in range(1, page+1):
    code = requests.get(f'https://api.github.com/repos/{repos}/commits?page={x}&per_page={per_page}').json()
    try:
        for y in code:
            if not y['commit']['author']['email'].endswith('github.com'):
                email.add(y['commit']['author']['email'])
            if not y['commit']['committer']['email'].endswith('github.com'):
                email.add(y['commit']['committer']['email'])
    except TypeError:
        pass

for x in email:
    print(x)