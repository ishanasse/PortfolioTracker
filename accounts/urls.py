from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.register, name="register"),
    path("logged_in", views.logged_in, name="logged_in"),
    path("logout", views.logout, name="logout"),
]
