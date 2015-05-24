from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from dashboard.views import render
from dashboard.models import SiteOptions

from .models import EmailSubscriber

VERIFICATION_EMAIL ="""
You're so close to getting a mailbox full of sweet, sweet comics!

Verify that you own this e-mail address by following this link:

{}

If you've no idea what this e-mail is about, just ignore it;
Somebody probably put your e-mail address into my subscribe box accidentally.
I won't send you any mail unless you follow the verification url.

"""

def _unsubscribe_url(request, subscriber):
    return request.build_absolute_uri(reverse('publish.views.unsubscribe_email',
                                              kwargs={'email':subscriber.email}))

def _verify_url(request, subscriber):
    return request.build_absolute_uri(reverse('publish.views.verify',
                                              kwargs={'email':subscriber.email,
                                                      'verification_code':subscriber.verification_code}))



def subscribe(request):
    """ A page detailing all of the fantastic ways one can subscribe """
    return render(request, 'publish/subscribe.html')

def subscribe_email(request):
    """ POST an e-mail address to subscribe """
    if request.POST and request.POST['email']:
        email = request.POST['email'].strip(' ')
        try:
            subscriber = EmailSubscriber.objects.get(email=email)
        except EmailSubscriber.DoesNotExist:
            subscriber = EmailSubscriber(email=email)
            subscriber.save()

        siteoptions = SiteOptions.get()
        verify_url = _verify_url(request, subscriber)
        message = VERIFICATION_EMAIL.format(verify_url)
        subscriber.send_mail(subject="Welcome to {}!".format(siteoptions.title),
                             message=message,
                             unsubscribe_url=_unsubscribe_url(request, subscriber))

        return render(request, "publish/subscribe_success.html", {'email':email})
    else:
        return HttpResponseRedirect(reverse("publish.views.subscribe"))

def verify(request, email, verification_code):
    try:
        e = EmailSubscriber.objects.get(email=email, verification_code=verification_code)
        e.verified = True
        e.save()
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
    return render(request, "publish/manage.html", {'subscribers':subscribers})


