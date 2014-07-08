#stdlib imports
import re

#django imports
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.conf import settings

#local imports
from bloomlist.views import bloom_view
from random_name import name

REQUIRED_FIELD = "This is a required field."
USERNAME_ALREADY_EXISTS = "This username already exists. Please choose another." 
USERNAME_LOWER = "The username must be lowercase."
USERNAME_REGEX = "The username can only contain characters, numbers, the" + \
                    " underscore, and that's it."
INVALID_EMAIL = "I'm pretty sure that's an invalid email."


def home(request):
    return render(request, "dashboard/home.html", {'random_name':name()})


def login_view(request):
    context = {}
    context['random_name'] = name()
    nxt = request.GET.get('next', False)
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if nxt:
                    return HttpResponseRedirect(nxt)
                else:
                    return HttpResponseRedirect(reverse(settings.AFTER_LOGIN_GO_HERE))
            else:
                return HttpResponseRedirect(reverse('dashboard.views.disabled'))
        else:
            context['error'] = "Nope. Didn't work. Try again?"
    return render(request, "dashboard/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('dashboard.views.home'))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        email = request.POST.get('email', False)

        errors = False
        context = {}
        context['username'] = username
        context['email'] = email
        context['username_errors'] = []
        context['password_errors'] = []
        context['email_errors'] = []

        if not username or not password or not email:
            errors = True
            if not username:
                context['username_errors'].append(REQUIRED_FIELD)
            if not password:
                context['password_errors'].append(REQUIRED_FIELD)
            if not email:
                context['email_errors'].append(REQUIRED_FIELD)

        if username and not username.islower():
            errors = True
            context['username_errors'].append(USERNAME_LOWER)

        regex = re.compile(r'^[a-z-_0-9]+$')
        if username and not regex.match(username):
            errors = True
            context['username_errors'].append(USERNAME_REGEX)

        if not errors:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
            except IntegrityError:
                errors = True
                context['username_errors'].append(USERNAME_ALREADY_EXISTS)

        if email and (not "@" in email or not "." in email):
            errors = True
            context['email_errors'].append(INVALID_EMAIL)

        if errors:
            return render(request, "dashboard/register.html", context)
        else:
            return HttpResponseRedirect(reverse(settings.AFTER_LOGIN_GO_HERE))

    return render(request, "dashboard/register.html", {'random_name':name()})

def users_bloom(request):
    list_of_users = [u.username for u in User.objects.all()]
    return bloom_view(name="user", 
                      list_of_strings=list_of_users,
                      request=request)
