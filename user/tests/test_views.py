from django.test import TestCase, Client
from django.urls import reverse
from user.models import User
import json
from rest_framework import status
class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()


    def test_user_registration_GET(self):
        client = self.client
        response = client.get(reverse("user_register"))
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_registration_POST(self):
        client = self.client
        response = client.post(reverse("user_register"),{
            "username":"testuser",
            "password": "fooboo12"
        })
        # print(response.json())
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.first().username, "testuser")

    def test_user_repeation(self):
        client = self.client
        response = client.post(reverse("user_register"),{
            "username":"repeatuser",
            "password": "fooboo12"
        })
        # print(response.json())
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.first().username, "repeatuser")

        response = client.post(reverse("user_register"),{
            "username":"repeatuser",
            "password": "fooboo12"
        })
        # print(response.json())
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


    """def test_user_registration_small_uname_POST(self):
        client = self.client
        response = client.post(reverse("user_register"),{
            "username":"te",
            "password": "fooboo12"
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)"""

    def test_user_registration_small_password_POST(self):
        client = self.client
        response = client.post(reverse("user_register"),{
            "username":"testuser123",
            "password": "foo"
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_registration_small_password_POST(self):
        client = self.client
        response = client.post(reverse("user_register"),{
            "username":"",
            "password": "foo"
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    # USERNAME greater than 25 chars
    def test_user_registration_large_username_POST(self):
        client = self.client
        response = client.post(reverse("user_register"),{
            "username":"abcdefghijklmnopqrstuvxyzabc",
            "password": "foo"
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)    
