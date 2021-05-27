from django.db.models.fields import CommaSeparatedIntegerField
from rest_framework import serializers
from tweetme2.settings import ALLOWED_HOSTS
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
# import random
from .models import Tweet
from .form import Tweet, TweetForm
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views h
def home_view(request, *args, **kwargs):
    return render(request,"pages/home.html", context={} , status = 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([SessionAuthentication])
def tweet_creat_view(request, *args,**kwargs):
    serializer = TweetSerializer(data = request.POST)
    if serializer.is_valid(raise_exception= True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status = 400)


@api_view(['GET'])
def tweet_list_view(request, *args , **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs , many = True)
    return Response(serializer.data, status= 201)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args , **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status= 404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status = 201)


@api_view(['GET','DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args , **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    print(qs)
    if not qs.exists():
        return Response({}, status= 404)
    qs = qs.filter(user = request.user)
    if not qs.exists():
        return Response({"message":"You can not delete this tweet"}, status= 401)
    print(qs)
    obj = qs.first()
    obj.delete()
    # serializer = TweetSerializer(obj )
    return Response({"messgae":"Tweet removed "}, status = 201)








def tweet_creat_view_pure_django(request,*args,**kwargs):
    """ REST api view """
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status = 401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    # print("ajax ---> ",request.is_ajax())
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201) #201 == created items 

        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors , status = 400)
    return render(request,"components/forms.html",context={"form":form})


def tweet_list_view_pure_django(request, *args , **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {
        "isUser":False,
        "response": tweet_list,
    }
    return JsonResponse(data)

def tweet_detail_view_pure__django(request, tweet_id,*args,**kwargs):
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