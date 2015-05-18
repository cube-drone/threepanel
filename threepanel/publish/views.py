from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, NoReverseMatch

from dashboard.views import render
from dashboard.models import SiteOptions

from .models import EmailSubscriber

# Create your views here.
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

        try:
            siteoptions = SiteOptions.get()
            verify_url = request.build_absolute_uri(reverse('publish.views.verify',
                            kwargs={'email':subscriber.email,
                                    'verification_code':subscriber.verification_code}))
            message = render(request, 'publish/verification_email.txt', {
                                'verify_url':verify_url,
                                'dashboard':siteoptions})
            subscriber.send_mail(subject="Welcome to {}!".format(siteoptions.title),
                                 message=message,
                                 unsubscribe_url=request.build_absolute_uri(
                                    reverse('publish.views.unsubscribe_email')))
        except NoReverseMatch:
            return HttpResponseRedirect(reverse("publish.views.bad_email"))

        return render(request, "publish/subscribe_success.html", {'email':email})
    else:
        return HttpResponseRedirect(reverse("publish.views.subscribe"))

def bad_email(request):
    return render(request, "publish/bad_email.html")

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
