import json
from rest_framework.test import APITestCase, APIClient
from user.models import User
from django.urls import reverse
from movie_collection.serializers import MovieCollectionSerializer
from movie_collection.models import MovieCollection
from user.utils import generate_jwt_token
# from requests.auth import HTTPBasicAuth
from django.test import TestCase, Client
import requests
from rest_framework import status
from . import collection_json_strings

class MovieList_authenticated(APITestCase):

    #initial configuration
    def setUp(self):
        self.list_url = reverse("movie-list")
        response = self.client.post(reverse("user_register"), {
            "username": "testmovielist",
            "password": "fooboo12"
        })
        self.token = response.json()["access_token"]

    #check if the user is autenticated to fetch movie list
    def test_get_movie_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    #get movie list without authentication
    def test_get_movie_list_without_auth(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MovieCollection_auth(APITestCase):

    #initial configuration
    def setUp(self):
        response_user1 = self.client.post(reverse("user_register"), {
            "username": "testcollectionuser",
            "password": "fooboo12"
        })
        self.token_user1 = response_user1.json()["access_token"]
        response_user2 = self.client.post(reverse("user_register"), {
            "username": "testcollectionuser2",
            "password": "fooboo12"
        })
        self.token_user2 = response_user2.json()["access_token"]


        self.collection_url = reverse("movie-collection")

        self.collection_json = collection_json_strings.COLLECTION_JSON
        self.empty_title_collection = collection_json_strings.EMPTY_TITLE_COLLECTION_JSON


    def test_get_empty_collection_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user1}')
        response = self.client.get(self.collection_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        collections = response.json()["data"]["collections"]
        self.assertEquals(collections, [])

    def test_get_empty_collection_without_auth(self):
        response = self.client.get(self.collection_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #add collection without authentication
    def test_add_collection_without_auth(self):
        response = self.client.post(self.collection_url, json.loads(
            self.collection_json), format="json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #add collection and retrive it 
    def test_add_collection_and_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user1}')
        response = self.client.post(self.collection_url, json.loads(
            self.collection_json), format="json")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.collection_uuid = response.json()["collection_uuid"]
        
        response = self.client.get(
            reverse(
                "movie-collection_read_update_delete",
                kwargs={"uuid": self.collection_uuid}
            )
        )
        collections = response.json()["collections"]
        self.assertEquals(collections["uuid"], self.collection_uuid)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user1}')
        response = self.client.get(self.collection_url)
        collections = response.json()["data"]["collections"][0]
        self.assertEquals(collections["uuid"], self.collection_uuid)


    def test_access_other_users_collection(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user1}')
        response = self.client.post(self.collection_url, json.loads(
            self.collection_json), format="json")
        
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.collection_uuid = response.json()["collection_uuid"]
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user2}')
        response = self.client.get(
            reverse(
                "movie-collection_read_update_delete",
                kwargs={"uuid": self.collection_uuid}
            )
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


    

    

