from django.contrib import admin
from .models import post_table,userprofile,comments

class postadmin(admin.ModelAdmin):
    list_display=['user','post']   
admin.site.register(post_table,postadmin)

class profileadmin(admin.ModelAdmin):
    list_display=['username','email','firstname','lastname','profile_pic']
admin.site.register(userprofile,profileadmin)  

class commentadmin(admin.ModelAdmin):
    list_display=['user','comment','date']
admin.site.register(comments,commentadmin)
