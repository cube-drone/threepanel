import sys

from django.shortcuts import render as django_render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import SiteOptions
from .forms import SiteOptionsForm


def render(request, template, options):
    dashboard = SiteOptions.get()
    f_code = sys._getframe(1).f_code
    dashboard.caller = f_code.co_name
    dashboard.filename = f_code.co_filename
    options['dashboard'] = dashboard
    return django_render(request, template, options)


def site_options(request):
    site_options = SiteOptions.get()
    if request.method == 'POST':
        form = SiteOptionsForm(request.POST, instance=site_options)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Options Updated!')
            return HttpResponseRedirect(reverse("dashboard.views.site_options"))
    else:
        form = SiteOptionsForm(instance=site_options)

    return render(request, 'dashboard/site_options.html', {'form': form})


def login(request):
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username or not password:
            messages.add_message(request, messages.ERROR,
                                 'No username or password provided.')
            return render(request, "dashboard/login.html", {})

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

    return render(request, "dashboard/login.html", {})
