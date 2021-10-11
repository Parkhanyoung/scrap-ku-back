from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    """Test User model"""

    def test_create_valid_user(self):
        """Test creating a user with valid info succeeds"""
        payload = {
            'email': 'test@naver.com',
            'password': 'test123',
            'name': 'phanyoung'
        }
        user = get_user_model().objects.create_user(**payload)
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotEqual(user.password, payload['password'])
        self.assertEqual(user.name, payload['name'])

    def test_user_email_normalized(self):
        """Test user email is normalized"""
        payload = {
            'email': 'test@NAVER.COM',
            'password': 'test123',
        }
        user = get_user_model().objects.create_user(**payload)
        email = payload['email']

        self.assertEqual(user.email, email.lower())

    def test_create_invalid_user(self):
        """Test creating a user with invalid info fails"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Test creating a superuser works well"""
        payload = {
            'email': 'test@NAVER.COM',
            'password': 'test123',
        }
        user = get_user_model().objects.create_superuser(**payload)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
