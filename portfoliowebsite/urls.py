from django.contrib import admin
from django.urls import path
from .views import Portfolio, SearchToAdd
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('', login_required(Portfolio.as_view())),
    path("", Portfolio.as_view()),
    path("add/", SearchToAdd.as_view()),
]
