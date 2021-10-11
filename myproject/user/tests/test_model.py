from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test User model"""

    def test_create_valid_user(self):
        """Test create a user object with valid info"""
        payload = {
            'email': 'test@naver.com',
            'password': 'test123',
            'name': 'phanyoung'
        }