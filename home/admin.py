from django.contrib import admin
from .models import post_table,userprofile,comments



class profileadmin(admin.ModelAdmin):
    list_display=['username','email','firstname','lastname','profile_pic']
admin.site.register(userprofile,profileadmin)  


