from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User,auth
from home.models import userprofile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        pswd=request.POST['pswd']
        
        user=auth.authenticate(username=uname,password=pswd)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('auth:login')
    return render (request,'login.html')



def register(request):
    if request.method=='POST':
       
        uname=request.POST['uname']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        bio=request.POST['bio']
        pswd=request.POST['pswd']
        cpswd=request.POST['cpswd']
        if pswd==cpswd:
            if User.objects.filter(username=uname).exists():
                messages.info(request,'username is already taken')
                return redirect('auth:register')
            else:    
                user=User.objects.create_user(username=uname,password=pswd)  
                profile=userprofile.objects.create(username=uname,firstname=fname,lastname=lname,email=email,bio=bio) 
                user.save()
                profile.save()
                return redirect('auth:login')

        else:
            messages.info(request,'passwords didint match')
            return redirect('auth:register')    

                
    return render(request,'register.html')    


@login_required(login_url='auth/')
def  logout(request):
    if request.method =='POST':    
        auth.logout(request)
        return redirect('/')

    return redirect('/')