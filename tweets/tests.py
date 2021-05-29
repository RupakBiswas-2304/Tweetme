from django.http import response
from django.test import TestCase, client
from django.contrib.auth import get_user_model


from rest_framework.test import APIClient


from .models import Tweet
# Create your tests here.

User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user =  User.objects.create_user(username = 'cfe', password = 'somepassword')
        Tweet.objects.create(content = "my 1st test ", user = self.user)

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content = "my 2nd test ", user = self.user)
        self.assertEqual(tweet_obj.id,2)
        self.assertEqual(tweet_obj.user, self.user)
        
    def get_client(self):
        client = APIClient()
        client.login(username = self.user.username, password = "somepassword")
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()),1)
        
        print(response.json())