from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from portfoliowebsite.models import TickerModel
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.
class Portfolio(View):

    def get(self, request):
        stocks = TickerModel.objects.all()
        return render(request, "portfolio.html", {"stocks":stocks})

    def post(self, request):
        title = request.POST["title"]
        category = request.POST["category"]
        #author = request.POST["author"]
        author = request.user
        content = request.POST["content"]
        
        TickerModel.objects.create(title = title, category=category.upper(), author=author, content=content, created_at=datetime.now())
        return redirect("/articles/") 


class AddToPortfolio(View):

    def get(self, request):
        return render(request, "addtoportfolio.html")

    def post(self, request):
        title = request.POST["title"]
        category = request.POST["category"]
        #author = request.POST["author"]
        author = request.user
        content = request.POST["content"]
        
        ArticleModel.objects.create(title = title, category=category.upper(), author=author, content=content, created_at=datetime.now())
        return redirect("/portfolio/") 