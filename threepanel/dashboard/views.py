from django.shortcuts import render


def home(request):
    return render(request, "dashboard/home.html", {})

def login(request):
    return render(request, "dashboard/login.html", {})

def register(request):
    return render(request, "dashboard/register.html", {})

def console(request):
    pass
