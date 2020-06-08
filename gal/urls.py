from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('panel', views.panel, name='panel'),
    path('logout', views.logout, name='logout'),
    path('upload', views.upload, name='upload'),
    path('create_category', views.create_category, name='create_category'),
]

