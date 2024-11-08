from rest_framework.test import APITestCase
from .models import StreamPlatform, WatchList, Review
from django.urls import reverse
from rest_framework import status
# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#from movie_rating import models

class StreamPlatformTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='example', password='example123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATIONS='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(name="Netflix", about="#1 no website", website="https://netflix.com")


    def test_StreamPlatform_create(self):
        data ={
            'name': 'netflix',
            'about': '1 no stream platform',
            'website': 'https://netflix.com'
        }

        response = self.client.post(reverse('stream-platform'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_StreamPlatform_list(self):
        response = self.client.get(reverse('stream-platform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_StreamPlatform_ind(self):
        response = self.client.get(reverse('stream-platform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="example123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(name="Netflix", about="#1 website", website="https://netflix.com")
        self.watchlist = WatchList.objects.create(title='example movie', description='nice movie', platform=self.stream, active=True)

    def test_WatchList_create(self):
        data = {
            'title': 'example movie',
            'description': 'nice movie',
            'platform': self.stream,
            'active': True
        }

        response = self.client.post(reverse('watch-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_WatchList_list(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_WatchList_ind(self):
        response = self.client.get(reverse('watch-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WatchList.objects.count(), 1)
        self.assertEqual(WatchList.objects.get().title, 'example movie')



class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="example123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(name="Netflix", about="#1 website", website="https://netflix.com")
        self.watchlist = WatchList.objects.create(title='example movie', description='nice movie', platform=self.stream, active=True)
        self.watchlist2 = WatchList.objects.create(title='example movie', description='nice movie', platform=self.stream,
                                                  active=True)
        self.review = Review.objects.create(review_user=self.user, rating=5, description="great movie!", watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "great movie",
            "watchlist": self.watchlist,
            "active": True

        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)


        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "great movie-updated",
            "watchlist": self.watchlist,
            "active": False

        }

        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

