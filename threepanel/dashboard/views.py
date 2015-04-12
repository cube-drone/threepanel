import sys

from django.shortcuts import render as django_render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def render(request, template, options):
    f_code = sys._getframe(1).f_code
    caller = f_code.co_name
    filename = f_code.co_filename
    options['dashboard'] = {'caller': caller, 
                            'filename': filename}
    return django_render(request, template, options)


def login(request):
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username or not password:
            messages.add_message(request, messages.ERROR, 
                                 'No username or password provided.')
            return render(request, "login.html", {}) 
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('comics.views.manage'))
            else:
                messages.add_message(request, messages.ERROR, 
                                     'Your account has been disabled.')
        else:
            messages.add_message(request, messages.ERROR, 
                                 'Authentication failed!')

    return render(request, "login.html", {}) 
