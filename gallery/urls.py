from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('post/<slug:slug>', views.post, name='post'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<slug:slug>', views.update_post, name='update_post'),
    path('delete_post/<slug:slug>', views.delete_post, name='delete_post'),
    path('mail/', views.mail, name='mail'),
    path('sendMail/', views.sendMail, name='sendMail'),
]

