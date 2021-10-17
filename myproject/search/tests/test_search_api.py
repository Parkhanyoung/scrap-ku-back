from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from scrap.models import Courdiv, College, ElectivesGroup, Department
from scrap.serializers import CourdivSerializer, CollegeSerializer, \
                              GroupSerializer, DeptSerializer

from rest_framework.test import APIClient
from rest_framework import status


COURDIV_URL = reverse('search:search-courdiv')
COLLEGE_URL = reverse('search:search-college')
GROUP_URL = reverse('search:search-group')
DEPT_URL = reverse('search:search-dept')


def create_courdiv(name):
    courdiv = Courdiv.objects.create(
        name=name,
        code='00',
        rowid='1',
        final_opt='dept'
    )
    return courdiv


def create_college(name, courdiv):
    college = College.objects.create(
        name=name,
        code='0001',
        rowid='1',
    )
    college.courdiv.add(courdiv)
    return college


def create_group(name, courdiv):
    group = ElectivesGroup.objects.create(
        name=name,
        code='0001',
        rowid='1',
        courdiv=courdiv
    )
    return group


def create_dept(name, courdiv, college):
    dept = Department.objects.create(
        name=name,
        code='0001',
        college=college
    )
    dept.courdiv.add(courdiv)
    return dept


class SearchCategoryTest(TestCase):
    """Test seaching categories [courdiv, college, group]"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@naver.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_search_courdiv(self):
        """Test searching courdiv"""
        create_courdiv('전공')
        courdivs = Courdiv.objects.all()
        serializer = CourdivSerializer(courdivs, many=True)
        res = self.client.get(COURDIV_URL)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_search_college(self):
        """Test searching college"""
        courdiv = create_courdiv('전공')
        create_college('사범대학', courdiv)
        courdiv = create_courdiv('학문의기초')
        create_college('경영대학', courdiv)
        colleges = College.objects.filter(courdiv__name='전공')
        serializer = CollegeSerializer(colleges, many=True)
        res = self.client.get(COLLEGE_URL, {'courdiv': '전공'})

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_search_group(self):
        """Test searching group"""
        courdiv = create_courdiv('교양')
        create_group('1학년세미나', courdiv)
        groups = ElectivesGroup.objects.filter(courdiv__name='교양')
        serializer = GroupSerializer(groups, many=True)
        res = self.client.get(GROUP_URL)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_search_dept(self):
        """Test searching departments"""
        courdiv = create_courdiv('전공')
        college1 = create_college('사범대학', courdiv)
        college2 = create_college('경영대학', courdiv)
        create_dept(
            name='영어교육과',
            courdiv=courdiv,
            college=college1
            )
        create_dept(
            name='경영학과',
            courdiv=courdiv,
            college=college2
        )
        depts = Department.objects.filter(
            courdiv__name='전공', college__name='사범대학'
            )
        serializer = DeptSerializer(depts, many=True)
        payload = {'courdiv': '전공', 'college': '사범대학'}
        res = self.client.get(DEPT_URL, payload)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)
