from django.contrib import admin
from django.urls import path

from TextcraftersApp import views

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/keywords/', views.get_keywords, name='get_keywords'),
]
