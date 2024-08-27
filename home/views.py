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

       

@login_required(login_url='auth/')
def profile(request,user):
    try:
        userdata=userprofile.objects.get(username=user)
        comment=comments.objects.all()
        current=request.user
        currentuser=userprofile.objects.get(username=current)
        
        posts=post_table.objects.filter(user__username=user).all()
        if currentuser.following.filter(username=userdata.username).exists():
            isfollowing=True
        else:
            isfollowing=False    
        context={
            'profile_data':userdata,
            'userprofile':currentuser,
            'posts':posts,
            'comments':comment,
            'isfollowing':isfollowing
        }
        return render(request,'profile.html',context)   
    except:
        return render (request,'profilewithoutlogin.html')

@login_required(login_url='auth/')
def addpost(request):
    post=post_table.objects.all()
    current=request.user
    currentuser=userprofile.objects.get(username=current)
    context={
        'posts':post,
        'userprofile':currentuser,
        }
    if request.method=='POST':
        post=request.POST['post']    
        caption=request.POST['caption']    
        user=request.user
        post_profile=userprofile.objects.get(username=user)
        
        upload=post_table.objects.create(user=user,post_profile=post_profile,caption=caption,post=post)
        if upload:

            upload.save()
            data={'post':post,'caption':caption,'user':user.username}
            return JsonResponse(data, safe=False)

        else:
            return JsonResponse({'data':'Something went wrong!!'})
        # return redirect('/')    
        


@login_required(login_url='auth/')
def like(request,id):
    if request.method=='POST':
        
        currentuser=request.user.id
        postid=id
        postinstance=post_table.objects.get(id=postid)
        
        if  postinstance.likes.filter(id=currentuser).exists():
        
            postinstance.likes.remove(request.user)
            
            postinstance.save()
            print('disliked')
            return JsonResponse({'data':'dsliked'},safe=False)
        else:
            postinstance.likes.add(request.user)
            postinstance.save()
            print('liked')            
            return JsonResponse({'data':'liked'},safe=False)


@login_required(login_url='auth/')
def dltepost(request,id):
    postinstance=post_table.objects.get(id=id)
    postinstance.delete()
    
    return redirect('/')  


@login_required(login_url='auth/')
def pdltepost(request,id,user):
    postinstance=post_table.objects.get(id=id)
    postinstance.delete()
    url="/profile/"+str(user)+"/"
   
    return redirect(url)
   

   
    