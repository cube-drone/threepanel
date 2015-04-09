from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
import logging
from .models import Comic

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("YOLO")

@login_required
def manage(request):
    backlog = Comic.backlog()
    archives = Comic.archives()
    hero = Comic.hero()
    return render(request, "comics/manage.html", {
        'backlog': backlog,
        'archives': archives,
        'hero': hero}) 


@login_required
def trash(request):
    trash = Comic.trash()
    pass

@login_required
def create(request):
    pass

@login_required
def update(request, slug):
    pass

@login_required
def delete(request, slug):
    comic = get_object_or_404(Comic, slug=slug)
    comic.delete()
    logger.info("{} deleted".format(comic))
    messages.add_message(request, messages.INFO, 
                         "\"{}\" Deleted".format(comic.title))
    return HttpResponseRedirect(reverse('comics.views.manage'))
    
