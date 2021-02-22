from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@csrf_protect
def register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}. Please login here."
            )
            return redirect("/")

    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def logout(request):

    auth.logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/")


@login_required
def logged_in(request):
    articles = ArticleModel.objects.all()
    return render(request, "logged_in.html", {"articles": articles})
