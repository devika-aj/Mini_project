from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('', views.home,name='home'),
    # path('home', views.withoutlogin,name='withoutlogin'),
    path('profile/<str:user>/',views.profile,name='profile'),
    path('like/<int:id>/',views.like,name='like'), 
    path('dltepost/<int:id>/',views.dltepost,name='dltepost'),
    path('pdltepost/<int:id>/<str:user>/',views.pdltepost,name='pdltepost'),   
    path('addpost/',views.addpost,name='addpost'),
]
