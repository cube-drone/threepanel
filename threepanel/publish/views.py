from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, NoReverseMatch

from dashboard.views import render

from .models import EmailSubscriber

# Create your views here.
def subscribe(request):
    """ A page detailing all of the fantastic ways one can subscribe """
    return render(request, "publish/subscribe.html")

def subscribe_email(request):
    """ POST an e-mail address to subscribe """
    if request.POST and request.POST['email']:
        email = request.POST['email'].strip(' ')
        try:
            e = EmailSubscriber.objects.get(email=email)
        except EmailSubscriber.DoesNotExist:
            e = EmailSubscriber(email=email)
            e.save()

        try:
            e.verify(request)
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

def unsubscribe_email(request):
    """ POST an e-mail address to unsubscribe """
    pass
