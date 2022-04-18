import re
import requests


email = set()
email_regex = '[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'
page = None
repos_api = 'https://api.github.com/repos'
repos_list = [
    'HDVinnie/Private-Trackers-Spreadsheet'
]

for repos in repos_list:
    page_list = requests.get(f'{repos_api}/{repos}/commits?page=1&')
    if page_list.status_code != 200:
        print(page_list.status_code, page_list.json()['message'])
        break
    else:
        page = int((re.findall('\d+\Z', page_list.links['last']['url']))[0])

    for x in range(1, page+1):
        code = requests.get(f'{repos_api}/{repos}/commits?page={x}').json()
        try:
            for y in code:
                email_author = y['commit']['author']['email']
                if not email_author.endswith('github.com'):
                    print(email_author)
                    email_re = re.findall(email_regex, email_author)
                    print(email_re)
                    # email.add(re.findall(email_regex, email_author))

                email_committer = y['commit']['committer']['email']
                if not email_committer.endswith('github.com'):
                    print(email_committer)
                    email_re = re.findall(email_regex, email_committer)
                    print(email_re)
                    # email.add(re.findall(email_regex, email_committer))
        except TypeError:
            pass

# for x in email:
#     print(x)