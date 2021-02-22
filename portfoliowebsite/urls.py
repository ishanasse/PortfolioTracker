from django.contrib import admin
from django.urls import path
from .views import Portfolio, SearchToAdd, HomePage

# from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('', login_required(Portfolio.as_view())),
    path("", HomePage.as_view()),
    path("portfolio/", Portfolio.as_view()),
    path("portfolio/add/", SearchToAdd.as_view()),
]
