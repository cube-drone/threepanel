from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins

from dashboard.views import render
from dashboard.models import SiteOptions

from slugify import slugify

import random_name
from .models import EmailSubscriber, SpamSpamSpamSpam, InvalidEmail


def subscribe(request):
    """ A page detailing all of the fantastic ways one can subscribe """
    random_email = "{}@sample.org".format(slugify(random_name.proper_name()))
    return render(request, 'publish/subscribe.html', {'random_email':random_email})

def subscribe_email(request):
    """ POST an e-mail address to subscribe """
    if request.POST and request.POST['email']:
        email = request.POST['email'].strip(' ')
        try:
            subscriber = EmailSubscriber.objects.get(email=email)
        except EmailSubscriber.DoesNotExist:
            try:
                subscriber = EmailSubscriber(email=email)
                subscriber.save()
            except InvalidEmail:
                return HttpResponseRedirect(reverse("publish.views.bad"))

        siteoptions = SiteOptions.get()
        try:
            subscriber.send_verification_email()
        except SpamSpamSpamSpam:
            return HttpResponseRedirect(reverse("publish.views.spam"))
        except NoReverseMatch:
            return HttpResponseRedirect(reverse("publish.views.bad"))

        return render(request, "publish/subscribe_success.html", {'email':email})
    else:
        return HttpResponseRedirect(reverse("publish.views.subscribe"))

def spam(request):
    return render(request, "publish/spam.html")

def bad(request):
    return render(request, "publish/bad.html")

def verify(request, email, verification_code):
    try:
        e = EmailSubscriber.objects.get(email=email, verification_code=verification_code)
        e.verified = True
        e.save()
        mail_admins(subject="Verified!",
                    message=email)
        return render(request, "publish/verify_success.html")
    except EmailSubscriber.DoesNotExist:
        return render(request, "publish/verify_failure.html")

def unsubscribe_email(request, email):
    try:
        e = EmailSubscriber.objects.get(email=email)
        e.delete()
        return render(request, "publish/unsubscribe.html")
    except EmailSubscriber.DoesNotExist:
        return render(request, "publish/unsubscribe.html")

@login_required
def manage(request):
    subscribers = EmailSubscriber.objects.all()
    number_of_subscribers = len(subscribers)
    return render(request, "publish/manage.html",
            {'subscribers':subscribers,
             'number_of_subscribers':number_of_subscribers})


