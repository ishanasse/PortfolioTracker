from django.contrib import admin
from django.urls import path
from .views import Portfolio, AddToPortfolio
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('', login_required(Portfolio.as_view())),
    path('', Portfolio.as_view()),
    path('add/', AddToPortfolio.as_view()),
]