# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Local imports
from bloomlist.views import bloom_view

# App
from .models import Account


def home(request):
    return render(request, "streams/base.html", {
        'siteroot':settings.ABSOLUTE_URL_BASE})


def accounts_bloom(request):
    list_of_accounts = [a.slug for a in Account.objects.all()]
    return bloom_view(name="account", 
                      list_of_strings=list_of_accounts,
                      request=request)
