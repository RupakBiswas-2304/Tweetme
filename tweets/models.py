from django.db import models
import random
from django.conf import settings
from django.db.models.deletion import CASCADE
# Create your models here.

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null = True, on_delete= models.SET_NULL)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    likes = models.ManyToManyField(User, related_name= 'tweet_user',blank = True, through= TweetLike)
    content = models.TextField(blank=True, null = True)
    image = models.FileField(upload_to = 'images/',blank=True, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # class __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None

    # def serialize(self):
    #     'Feel Free to delete'
    #     return {
    #         "id": self.id,
    #         "content":self.content,
    #         "Likes": random.randint(1,200),
    #     }