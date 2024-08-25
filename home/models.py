
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class userprofile(models.Model):
    username=models.CharField(max_length=200)
    firstname=models.CharField(blank=True,max_length=200)
    lastname=models.CharField(blank=True,max_length=200)
    email=models.EmailField(blank=True)
    profile_pic=models.ImageField(upload_to='profiles',default='profiles/img.jpg')
    followers=models.ManyToManyField(User,blank=True,related_name='followers')        
    following=models.ManyToManyField(User,blank=True,related_name='following')
    bio=models.CharField(max_length=200,blank=True)



