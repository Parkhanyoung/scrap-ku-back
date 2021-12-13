from . import auth_info
import requests
import json
import urllib3

# request 보낼 때 verify=False로 인한 warning 제거
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BaseScrapper:
    """Base scrapper which has common properties of other scrappers"""

    def __init__(self, attr):
        self.url = 'https://sugang.korea.ac.kr/view'
        self.cookies = {
            'JSESSIONID': auth_info.jsession_id('학번', '비밀번호')
        }
        self.headers = {
            'Referer': 'https://sugang.korea.ac.kr/core',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/94.0.4606.71 Safari/537.36',
        }
        self.params = {
            'attribute': attr,  # [ex. lectHakbuData, combo]
            'fake': auth_info.fake()
        }

    def scrap(self):
        """Scrap data from KU and return it"""
        res = requests.post(
            url=self.url,
            cookies=self.cookies,
            headers=self.headers,
            params=self.params,
            data=self.data,
            verify=False
            )
        scrap_data = json.loads(res.text)
        scrap_data = scrap_data['data']

        return scrap_data


class CollegeGroupScrapper(BaseScrapper):
    """Scrapper for collecting college / Electives group(pCol, pGroupCd)"""

    def __init__(self):
        super().__init__('combo')

    def set_data(self, courdiv_code=None):
        """Set arguments of data and return it"""
        # for college
        if courdiv_code:
            data = [
                ('obj', 'pCol'),
                ('args', 'KOR'),
                ('args', '2021'),
                ('args', '2R'),
                ('args', '1'),
                ('args', courdiv_code)
            ]
        # for electives group
        else:
            data = [
                ('obj', 'pGroupCd'),
                ('args', 'KOR'),
                ('args', '2021'),
                ('args', '2R'),
            ]
        self.data = data


class DeptScrapper(BaseScrapper):
    """Scrapper for collecting department data"""

    def __init__(self):
        super().__init__('combo')

    def set_data(self, col_code, cd_code):
        data = [
            ('obj', 'pDept'),
            ('args', 'KOR'),
            ('args', col_code),
            ('args', '2021'),
            ('args', '2R'),
            ('args', cd_code)
        ]
        self.data = data


class CourseScrapper(BaseScrapper):
    """Scrapper for collecting course data"""

    def __init__(self):
        super().__init__('lectHakbuData')

    def set_data(self, cd_code, dept_code='', group_code=''):
        data = [
            ('pYear', '2021'),
            ('pTerm', '2R'),
            ('pCampus', '1'),
            ('pGradCd', '0136'),
            ('pCourDiv', cd_code),
            ('pDept', dept_code),
            ('pGroupCd', group_code)
        ]
        self.data = data
