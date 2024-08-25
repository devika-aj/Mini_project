from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from .models import post_table,userprofile,comments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .form import profileform
from django.contrib import messages
# Create your views here.


# @login_required(login_url='auth/')
def home(request):
    try:
        post=post_table.objects.all() 
        story=post_table.objects.all()
        li=[]

        for i in story:
            ar={}
            ar['id']=i.id
            ar['post']=i.post[0:5]+"..." 
            ar['user']=i.user 
            ar['post_profile']=i.post_profile 
            ar['likes']=i.likes.all().count()
            li.append(ar)
        story=sorted(li, key=lambda x: x['likes'], reverse=True)[0:5]
        
        current=request.user
        
    
        currentuser=userprofile.objects.get(username=current)
        # print(currentuser)
        context={
            'posts':post,
            'userprofile':currentuser, 
            'user':current ,
            'story':story
            }

        return render(request,'feed.html',context)
    except:
        post=post_table.objects.all() 
        story=post_table.objects.all()
        li=[]

        for i in story:
            ar={}
            ar['id']=i.id
            ar['post']=i.post[0:5]+"..." 
            ar['user']=i.user 
            ar['post_profile']=i.post_profile 
            ar['likes']=i.likes.all().count()
            li.append(ar)
        story=sorted(li, key=lambda x: x['likes'], reverse=True)[0:5]
    
        context={
            'posts':post,
            'story':story
         }

        return render(request,'without_login.html',context) 

       
