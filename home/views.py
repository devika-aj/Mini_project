from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from .models import post_table,userprofile,comments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .form import profileform
from home.models import userprofile
from django.contrib import messages
import re
# Create your views here.



def register(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        password = request.POST.get('pswd')
        confirm_password = request.POST.get('cpswd')

        # Validation for username: only alphabets and special characters
        if not re.match(r'^[a-zA-Z@_!#$%^&*()<>?/\|}{~:;,.]*$', username):
            messages.error(request, "Username can only contain alphabets and special characters.")
            return render(request, 'auth/register.html')

        # Validation for first name and last name: only alphabets
        if not first_name.isalpha():
            messages.error(request, "First name can only contain alphabets.")
            return render(request, 'auth/register.html')

        if not last_name.isalpha():
            messages.error(request, "Last name can only contain alphabets.")
            return render(request, 'auth/register.html')

        # Validation for password: at least 7 characters
        if len(password) < 7:
            messages.error(request, "Password must be at least 7 characters long.")
            return render(request, 'auth/register.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'auth/register.html')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'auth/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'auth/register.html')

        # Create user and userprofile
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user_profile = userprofile.objects.create(username=username, firstname=first_name, lastname=last_name, email=email, bio=bio)

        messages.success(request, "Your account has been created successfully!")
        return redirect('auth:login')

    return render(request, 'auth/register.html')

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
        
    
    # return render(request,'feed.html',context)    

@login_required(login_url='auth/')
def edit(request):
    userdata=userprofile.objects.get(username=request.user)
   
    post=post_table.objects.all()
 
    current=request.user
    currentuser=userprofile.objects.get(username=current)
    edit_instance=profileform(request.POST or None, request.FILES or None,instance=currentuser)

    context={
        'posts':post,
        'userprofile':currentuser,
        'form':edit_instance,
         }
    if edit_instance.is_valid():
        
        edit_instance.save()
        return redirect('/')


    return render(request,'profileupdate.html',context)

@login_required(login_url='auth/')
def search(request):
    currentuser=userprofile.objects.get(username=request.user)
    context={
                'userprofile':currentuser,
                'data':'',
         
                    }
  
    if 'query' in request.GET:
        q=request.GET['query']
        # uname=User.objects.filter(username__icontains=q)

        res=userprofile.objects.filter(firstname__icontains=q) | userprofile.objects.filter(lastname__icontains=q) 
   
        if res is not None:
            context={
                'userprofile':currentuser,
                'data':res,
                # 'uname':uname
                    }
        else:
            context={
            'userprofile':currentuser,
            'data':res,
                    }  
        return render(request,'search.html',context)
                    
    return render(request,'search.html',context)


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
def follow(request,user):
    userdata=userprofile.objects.get(username=user)
    followerid=User.objects.get(username=userdata.username)

    current=request.user.username
    currentuserobject=userprofile.objects.get(username=current)
    
    if currentuserobject.following.filter(username=followerid).exists():
     
        currentuserobject.following.remove(followerid)
        userdata.followers.remove(request.user)
        print("unfollow")
        return JsonResponse("notfollowing",safe=False)
    else:
        print("follow")
        currentuserobject.following.add(followerid)
        userdata.followers.add(request.user)
        return JsonResponse("following",safe=False)

  
@login_required(login_url='auth/')
def comment(request,id):
    
    post=post_table.objects.get(id=id)
    currentuser=userprofile.objects.get(username=request.user)
    postcomments=comments.objects.filter(post=post)
    print(currentuser)
    context={
            'comments':postcomments,
            'userprofile':currentuser,
            'posts':post,
    }

    if request.method=='POST':
            comment=request.POST['comment']
            commentinstance=comments.objects.create(post=post,user=currentuser,comment=comment)
            commentinstance.save()
            date=comments.objects.get(id=commentinstance.id).date
            profile=currentuser.profile_pic.url
            data={
                'date':date,
                'comment':comment,
                'profile':profile,
                'user':currentuser.username,
                'id':commentinstance.id,
                'userid':currentuser.id
                }
            return JsonResponse(data, safe=False)
    

    return render(request,'comments.html',context) 


@login_required(login_url='auth/')
def deletecomment(request,id):
    print(id)
    commentinstance=comments.objects.get(id=id)
    currentuser=userprofile.objects.get(username=request.user)
    postcomments=comments.objects.filter(post=commentinstance.post)
    post=commentinstance.post

    commentinstance.delete()
    context={
            'comments':postcomments,
            'userprofile':currentuser,
            'posts':post,
    }
    url="/comment/"+str(post.id)+"/"
    return redirect(url)



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
   

   
    