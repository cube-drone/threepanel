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


def domain_multiplex(f):
    """
    Check if we're coming in from a domain that has a SiteOptions object
    associated with it. If we're not, bounce us to home.

    If there's an associated SiteOptions object, load it into
    request.site

    We can fool the dashboard's domain assignment by setting FAKE_DOMAIN
    in the GET parameters or as a cookie. Setting a persistent cookie is
    a great way to test the site.
    """
    @wraps(f)
    def func_wrapper(request, *args, **kwargs):

        if 'fake_domain' in request.GET:
            domain = request.GET['fake_domain']
        elif 'FAKE_DOMAIN' in request.GET:
            domain = request.GET['FAKE_DOMAIN']
        elif 'fake_domain' in request.COOKIES:
            domain = request.COOKIES['fake_domain']
        elif 'FAKE_DOMAIN' in request.COOKIES:
            domain = request.COOKIES['FAKE_DOMAIN']
        elif 'HTTP_HOST' in request.META:
            domain = request.META['HTTP_HOST']
        else:
            log.warning("No HTTP Host in request.")
            return HttpResponseRedirect(reverse(all_sites))

        request.site = SiteOptions.get(domain)
        if request.site:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(all_sites))
    return func_wrapper

def creator_login_required(f):
    """
    We're a creator, so we want to know which set of sites we manage.
    This makes the assumption that the first argument to ANY creator view
    is going to be the site_slug, which is a dangerous assumption.
    It throws a nasty error when it fails so hopefully we can catch that.
    It sets request.site (the current site being worked on)
    and request.sites (all sites available to the user)
    """
    @login_required
    @wraps(f)
    def func_wrapper(request, *args, **kwargs):
        if not request.user:
            log.warning("Creator Dashboard requires a user object.")
            return HttpResponseRedirect(reverse(all_sites))

        request.sites = SiteOptions.getForUser(request.user)

        site_slug = args[0]
        matching_sites = request.sites.filter(slug=site_slug)
        if len(matching_sites) == 0:
            log.error("User {} trying to log into site {}".format(request.user, site_slug))
            request.site = None
        else:
            request.site = matching_sites[0]

        if request.sites and request.site:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(creator_home))
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
    dashboard['type'] = 'home'

    #The stuff that gets set in @creator_login_required
    try:
        sites = request.sites
        dashboard['sites'] = request.sites
    except AttributeError:
        log.debug("request.sites not set during render phase.")
    except TypeError:
        log.debug("request.sites not set during render phase.")

    #The stuff that gets set in @domain_multiplex
    try:
        site_options = request.site
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
            dashboard['twitter_username'] = site_options.twitterintegration.username
            dashboard['twitter_widget_id'] = site_options.twitterintegration.widget_id
        except ObjectDoesNotExist:
            log.debug("request.sites.twitter not set during render phase.")
            dashboard['twitter_username'] = ""
            dashboard['twitter_widget_id'] = ""
    except AttributeError:
        log.debug("request.site not set during render phase.")
    except TypeError:
        log.debug("request.site not set during render phase.")

    # The stuff that always gets set
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
            is_working, status_message = twitter_integration.get_status()
            if is_working:
                messages.add_message(request, messages.SUCCESS, status_message)
            else:
                messages.add_message(request, messages.ERROR, status_message)
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

@login_required
def creator_home(request):
    return render(reqeust, "dashboard/creator_home.html", {})
