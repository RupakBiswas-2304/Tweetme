from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
import random
from .models import Tweet
from .form import Tweet, TweetForm

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request,"pages/home.html", context={} , status = 200)

def tweet_creat_view(request,*args,**kwargs):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()
    return render(request,"components/forms.html",context={"form":form})


def tweet_list_view(request, *args , **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [{"id":x.id, "content":x.content,"Likes": random.randint(0,125)} for x in qs]
    data = {
        "isUser":False,
        "response": tweet_list,
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id,*args,**kwargs):
    #rest API view
    data = {
        "id": tweet_id,
    }
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    return JsonResponse(data, status = status)
    # return HttpResponse(f"<h1> Hello {tweet_id} -{obj.content}</h1>")