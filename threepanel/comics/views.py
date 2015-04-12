from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
import logging
from .models import Comic
from .forms import ComicForm

logger = logging.getLogger(__name__)

def home(request):
    hero = Comic.hero()
    return HttpResponse("YOLO")

@login_required
def manage(request):
    backlog = Comic.backlog()
    archives = Comic.archives()
    hero = Comic.hero()
    print(backlog)
    print(hero)
    print(archives)
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
    if request.method == 'POST':
        form = ComicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Comic Created!')
            return HttpResponseRedirect(reverse("comics.views.manage"))
    else:
        form = ComicForm()

    return render(request, 'comics/create.html', {'form':form})

@login_required
def update(request, slug):
    comic = get_object_or_404(Comic, slug=slug)
    if request.method == 'POST':
        form = ComicForm(request.POST, instance=comic)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Comic Updated!')
            return HttpResponseRedirect(reverse("comics.views.manage"))
    else:
        form = ComicForm(instance=comic)

    return render(request, 'comics/update.html', {'form':form, 'slug':slug})

@login_required
def delete(request, slug):
    comic = get_object_or_404(Comic, slug=slug)
    comic.delete()
    logger.info("{} deleted".format(comic))
    messages.add_message(request, messages.INFO, 
                         "\"{}\" Deleted".format(comic.title))
    return HttpResponseRedirect(reverse('comics.views.manage'))
    
