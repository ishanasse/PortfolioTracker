from django.contrib import admin
from django.urls import path
from .views import Portfolio, SearchToAdd, HomePage, PortfolioHistory, AllTransactions

from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('', login_required(Portfolio.as_view())),
    path("", HomePage.as_view()),
    path("portfolio/", login_required(Portfolio.as_view())),
    path("portfolio/add/", login_required(SearchToAdd.as_view())),
    path("portfolio/history/", login_required(PortfolioHistory.as_view())),
    path("portfolio/transactions/", login_required(AllTransactions.as_view())),
]
