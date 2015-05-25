import logging

from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dashboard.views import render

from .models import Comic, Blog
from .forms import ComicForm, BlogForm


logger = logging.getLogger(__name__)


def home(request):
    hero = Comic.hero()
    permalink = _permalink(request, hero.slug)
    return render(request,
                  "comics/single.html",
                  {'slug': hero.slug,
                   'permalink': permalink,
                   'comic':hero})


def single_by_numerical_order(request, n):
    """ redirect to single by slug """
    if int(n) <= 0:
        raise Http404("There's no Comic 0.")
    comic = get_object_or_404(Comic, order=n)
    return HttpResponseRedirect(reverse("comics.views.single",
                                kwargs={'comic_slug': comic.slug}))

def _permalink(request, comic_slug):
    return request.build_absolute_uri(reverse('comics.views.single',
                                              kwargs={'comic_slug':comic_slug}))


def single(request, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)
    if comic.hidden:
        raise Http404("For whatever reason, I've removed this comic from circulation.")
    if timezone.now() < comic.posted:
        raise Http404("This comic hasn't been posted yet!")
    permalink = _permalink(request, comic_slug)
    return render(request, "comics/single.html", {'preview': False,
                                                  'slug': comic_slug,
                                                  'permalink': permalink,
                                                  'comic': comic})

def archives(request):
    archives = Comic.archives()
    tags = Comic.all_tags()
    return render(request, "comics/archives.html", {'comics': archives,
                                                    'tags': tags})


def tag(request, slug):
    archives = Comic.archives().filter(tags__contains=[slug])
    tags = Comic.all_tags()
    return render(request, "comics/archives.html", {'comics': archives,
                                                    'active_tag': slug,
                                                    'tags': tags})

def search(request):
    try:
        search_term = request.GET['search']
    except KeyError:
        return HttpResponseRedirect(reverse("comics.views.archives"))
    comics = Comic.objects.search(search_term).filter(hidden=False)
    tags = Comic.all_tags()
    return render(request, "comics/archives.html", {'comics':comics,
                                                    'search_term': search_term,
                                                    'tags': tags})

def blog(request):
    archives = Comic.archives()
    blogs = []
    for comic in archives:
        for blog_post in comic.blog_posts:
            blogs.append(blog_post)
    return render(request, "comics/blog.html", {'blogs':blogs})

@login_required
def preview(request, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)
    return render(request, "comics/single.html", {'preview': True,
                                                  'slug': comic_slug,
                                                  'comic': comic})


@login_required
def manage(request):
    backlog = Comic.backlog()
    archives = Comic.archives()
    hero = Comic.hero()
    tags = Comic.all_tags()
    return render(request, "comics/manage.html", {
        'tags': tags,
        'backlog': backlog,
        'archives': archives,
        'hero': hero})

@login_required
def manage_tag(request, slug):
    backlog = Comic.backlog().filter(tags__contains=[slug])
    archives = Comic.archives().filter(tags__contains=[slug])
    tags = Comic.all_tags()
    return render(request, "comics/manage.html", {
        'tags': tags,
        'active_tag': slug,
        'backlog': backlog,
        'archives': archives})


@login_required
def trash(request):
    trash = Comic.trash()
    return render(request, "comics/manage_trash.html", {
        'trash': trash,
    })


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

    return render(request, 'comics/create.html', {'form': form})


@login_required
def update(request, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)
    print("Updating comic!")
    if request.method == 'POST':
        form = ComicForm(request.POST, instance=comic)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Comic Updated!')
            return HttpResponseRedirect(reverse("comics.views.manage"))
    else:
        form = ComicForm(instance=comic)

    return render(request, 'comics/update.html', {'form': form, 'slug': comic_slug})


@login_required
def delete(request, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)
    comic.hide()
    logger.info("{} deleted".format(comic))
    messages.add_message(request, messages.INFO,
                         "\"{}\" Deleted".format(comic.title))
    return HttpResponseRedirect(reverse('comics.views.manage'))


@login_required
def create_blog(request, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Blog Created!')
            return HttpResponseRedirect(reverse("comics.views.manage"))
    else:
        form = BlogForm(initial={'comic':comic})

    return render(request, 'comics/create_blog.html', {'form': form, 'comic_slug': comic_slug})


@login_required
def update_blog(request, comic_slug, slug):
    blog = get_object_or_404(Blog, comic__slug=comic_slug, slug=slug)
    print("Blog {} Updated".format(blog))
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Blog Updated!')
            return HttpResponseRedirect(reverse("comics.views.manage"))
    else:
        form = BlogForm(instance=blog)

    return render(request, 'comics/update_blog.html', {'form': form, 'comic_slug': comic_slug, 'slug': slug})


@login_required
def delete_blog(request, comic_slug, slug):
    blog = get_object_or_404(Blog, comic__slug=comic_slug, slug=slug)
    blog.hide()
    logger.info("{} deleted".format(blog))
    messages.add_message(request, messages.INFO,
                         "\"{}\" Deleted".format(blog.title))
    return HttpResponseRedirect(reverse('comics.views.manage'))
