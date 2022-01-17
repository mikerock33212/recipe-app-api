from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """test the users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test creating user with valid payload is successful"""
        payload = {
            'email' : 'mikerock@gmail.com',
            'password' : 'test123',
            'name' : 'testname'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """test creating user already exists fails"""
        payload = {'email':'mikerock@gmail.com', 'password':'testpass', 'name':'test'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test passwrod must be more than 5 char"""
        payload = {'email':'mikerock@gmail.com', 'password':'te', 'name':'test'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test a token is created for the user"""
        payload = {
            'email':'mikerock@gmail.com',
            'password':'test123',

        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """test token is notcreatec if invalid credentials given"""
        create_user(email='mickrock@gmail.com', password='test123')
        payload = {'email':'mikerock@gmail.com', 'password':'wrong'}
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test token is not created if user does not exist"""
        payload = {
            'email':'mikerock@gmail.com',
            'password':'test123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test email and passwrod are required"""
        res = self.client.post(TOKEN_URL, {'email':'one','password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)