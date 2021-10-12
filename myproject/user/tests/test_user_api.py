from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from user.serializers import UserSerializer


CREATE_USER_URL = reverse('user:user-list')
ME_URL = reverse('user:user-me')


def sample_user(**fields):
    """Create a sample user"""
    user = get_user_model().objects.create_user(**fields)
    return user


class UserApiTest(TestCase):
    """Test User Api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test create a new user"""
        payload = {
            'email': 'test@naver.com',
            'password': 'test123',
            'name': 'park'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

    def test_create_with_exsting_user_email(self):
        """Test creating a user with existing user-email fails"""
        payload = {
            'email': 'test@naver.com',
            'password': 'test123',
            'name': 'park'
        }
        sample_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_too_short_password(self):
        """Test creating a user with too short password" fails"""
        payload = {
            'email': 'test@naver.com',
            'password': '12345',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email=payload['email'])
            )


class PrivateUserApiTest(TestCase):
    """Test User Api (private)"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@naver.com',
            'test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_authorized(self):
        """Test retrieving a user succeeds"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user)
        self.assertEqual(res.data, serializer.data)

    def test_not_allowed_method(self):
        """Test post method is not allowed"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """Test updating a user succeeds"""
        payload = {
            'password': 'changed',
            'name': 'changed'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(self.user.name, payload['name'])
