import requests
import json
import urllib3
import auth_info

# request 보낼 때 verify=False로 인한 warning 제거
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fake = auth_info.fake()
jsessionID = auth_info.jsession_id('2018190220', 'gksdud15!')

cookies = {
    'JSESSIONID': jsessionID
}

headers = {
    'Referer': 'https://sugang.korea.ac.kr/core',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/94.0.4606.71 Safari/537.36',
}

params = {
    'attribute': 'lectHakbuData',
    'fake': auth_info.fake()
}


# 영교과 전공  [전공, 학문의기초 처리]
data = [
    ('pYear', '2021'),
    ('pTerm', '2R'),
    ('pCampus', '1'),
    ('pGradCd', '0136'),
    ('pCourDiv', '41'),
    ('pDept', ''),
    ('pGroupCd', '')
]

# [교양]
# data = [
#     ('pYear', '2021'),
#     ('pTerm', '2R'),
#     ('pCampus', '1'),
#     ('pGradCd', '0136'),
#     ('pCourDiv', '01'), #> cour_div 전공인지, 학문의 기초인지 등
#     ('pGroupCd', '24')  #> groupcd 교양 그룹 [ex. 1학년세미나 academic english]
# ]

# [군사학, 평생 ..]
# data = [
#     ('pYear', '2021'),
#     ('pTerm', '2R'),
#     ('pCampus', '1'),
#     ('pGradCd', '0136'),
#     ('pCourDiv', '41'), #> cour_div 전공인지, 학문의 기초인지 등
# ]

res = requests.post(
    'https://sugang.korea.ac.kr/view',
    cookies=cookies,
    headers=headers,
    params=params,
    data=data,
    verify=False
    )

res_str = json.loads(res.text)
print(res_str)
