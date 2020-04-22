from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "chat/index.html")

def login_view(request):
    return render(request, "chat/login.html")

def register(request):
    return render(request, "chat/register.html")