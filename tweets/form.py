from django.forms import ModelForm,ValidationError
from .models import Tweet

from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content)>MAX_TWEET_LENGTH:
            raise ValidationError("This tweet is to long")
        return content