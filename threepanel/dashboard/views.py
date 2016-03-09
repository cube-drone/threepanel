import sys
import datetime
from functools import wraps
import logging

from django.shortcuts import render as django_render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import SiteOptions, TwitterIntegration
from .forms import SiteOptionsForm, TwitterIntegrationForm


log = logging.getLogger('threepanel.{}'.format(__name__))


def dashboard(f):
    """
    Check if we're coming in from a domain that has a SiteOptions object
    associated with it. If we're not, bounce us to home.
    """
    @wraps(f)
    def func_wrapper(request, *args, **kwargs):
        request.site = SiteOptions.get(request)
        if request.site:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(all_sites))
    return func_wrapper


def unslugify(string):
    """
    >>> unslugify("create_event")
    "Create Event"
    """
    string = string.replace("_", " ")
    string_list = [x.capitalize() for x in string.split(" ")]
    return " ".join(string_list)


def render(request, template, options=None):
    if options is None:
        options = {}
    f_code = sys._getframe(1).f_code

    dashboard = {}
    try:
        site_options = request.site
        dashboard['site_options'] = request.site
        dashboard['title'] = site_options.title
        dashboard['slug'] = site_options.slug
        dashboard['tagline'] = site_options.tagline
        dashboard['elevator_pitch'] = site_options.elevator_pitch
        dashboard['author_name'] = site_options.author_name
        dashboard['author_website'] = site_options.author_website
        dashboard['google_tracking_code'] = site_options.google_tracking_code
        dashboard['youtube_channel'] = site_options.youtube_channel
        dashboard['patreon_page'] = site_options.patreon_page
        try:
            dashboard['twitter_username'] = site_options.twitter.username
            dashboard['twitter_widget_id'] = site_options.twitter.widget_id
        except AttributeError:
            pass
        except TypeError:
            pass
    except AttributeError:
        log.info("SiteOptions not set during render phase.")
    except TypeError:
        log.info("SiteOptions not set during render phase.")
    dashboard['favicon'] = settings.FAVICON
    dashboard['vagrant_hostname'] = settings.VAGRANT_HOSTNAME
    dashboard['site_title'] = settings.SITE_TITLE
    dashboard['site_url'] = settings.SITE_URL
    dashboard['caller'] = f_code.co_name
    dashboard['filename'] = f_code.co_filename
    dashboard['year'] = datetime.date.today().year
    dashboard['hide_nav'] = False
    dashboard['page_title'] = unslugify(dashboard['caller'].capitalize())

    log.info("{}:{}".format(dashboard['filename'], dashboard['caller']))

    # If any dashboard options are already set, they override the default settings
    # if they are not already set, set them!
    if 'dashboard' in options:
        dashboard.update(options['dashboard'])
    options['dashboard'] = dashboard

    return django_render(request, template, options)


@login_required
def site_options(request, site_slug):
    site_options = SiteOptions.objects.get(slug=site_slug)
    if request.method == 'POST':
        form = SiteOptionsForm(request.POST, instance=site_options)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Options Updated!')
            from comics.views import manage_redirect
            return HttpResponseRedirect(reverse(manage_redirect))
    else:
        form = SiteOptionsForm(instance=site_options)

    return render(request, 'dashboard/site_options.html', {'form': form, 'site_slug':site_slug})


@login_required
def twitter_integration(request, site_slug):
    site = SiteOptions.objects.get(slug=site_slug)
    if request.method == 'POST':
        try:
            twitter_integration = site.twitterintegration
            form = TwitterIntegrationForm(request.POST, instance=twitter_integration)
        except ObjectDoesNotExist:
            form = TwitterIntegrationForm(request.POST)
        if form.is_valid():
            twitter_integration = form.save(commit=False)
            twitter_integration.site = site
            twitter_integration.save()
            messages.add_message(request, messages.SUCCESS, 'Twitter Integration Updated!')
            return HttpResponseRedirect(site_options)
    else:
        try:
            twitter_integration = site.twitterintegration
            form = TwitterIntegrationForm(instance=twitter_integration)
        except ObjectDoesNotExist:
            form = TwitterIntegrationForm()

    return render(request, 'dashboard/twitter_integration.html', {'form': form, 'site_slug':site_slug})


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
                from comics.views import manage_redirect
                return HttpResponseRedirect(reverse(manage_redirect))
            else:
                messages.add_message(request, messages.ERROR,
                                     'Your account has been disabled.')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Authentication failed!')

    return render(request, "dashboard/login.html",  {'dashboard': {'hide_nav':True}})


def all_sites(request):
    sites = SiteOptions.objects.all()
    return render(request, "dashboard/all_sites.html", {'sites':sites})
