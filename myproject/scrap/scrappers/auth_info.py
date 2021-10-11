import requests
import time


def fake():
    fake = time.time() / 1000.0
    fake = str(fake).replace(".", "")[:13]
    return fake


def jsession_id(username, password):
    url = 'https://sugang.korea.ac.kr/login'

    headers = {
        'Referer': 'https://sugang.korea.ac.kr/login',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    params = {
        'attribute': 'loginChk',
        'fake': fake()
    }

    data = {
        'lang': 'KOR',
        'id': username,
        'pwd': password
    }

    res = requests.post(url, headers=headers, params=params, data=data)
    jsession_id = res.cookies['JSESSIONID']
    return jsession_id
