from django.db import models
import random
from django.conf import settings
from django.db.models.deletion import CASCADE
# Create your models here.

User = settings.AUTH_USER_MODEL
class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    content = models.TextField(blank=True, null = True)
    image = models.FileField(upload_to = 'images/',blank=True, null = True)
    
    # class __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content":self.content,
            "Likes": random.randint(1,200),
        }