from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from .models import User

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "chat/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid credentials."
            })
    else:
        return render(request, "chat/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(username, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")