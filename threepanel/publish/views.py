from dashboard.views import render

# Create your views here.
def subscribe(request):
    """ A page detailing all of the fantastic ways one can subscribe """
    return render(request, "publish/subscribe.html")

def subscribe_email(request):
    """ POST an e-mail address to subscribe """
    pass

def unsubscribe_email(request):
    """ POST an e-mail address to unsubscribe """
    pass
