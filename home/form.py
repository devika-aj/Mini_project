from django import forms
from .models import userprofile,post_table
from django.contrib.auth.models import User
class profileform(forms.ModelForm):
    class Meta:
        model=userprofile
        fields=['profile_pic','firstname','lastname','email','bio',]
     