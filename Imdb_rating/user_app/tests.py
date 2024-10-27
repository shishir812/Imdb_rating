from rest_framework.test import APITestCase
from django.urls import reverse

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    def test_register(self):
        data ={
            'username': 'abc',
            'email': 'abc@gmail.com',
            'password': 'abcd1234',
            'password2': 'abcd1234'
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="example123")

    def test_login(self):
        data ={
            'username': 'example',
            'password': 'example123'
        }

        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)




