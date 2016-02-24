import logging
import datetime

from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dashboard.views import render, dashboard

from dashboard.models import SiteOptions
from .models import Comic, Blog, Video, Image
from .forms import ComicForm, BlogForm, VideoForm, ImageForm


log = logging.getLogger('threepanel.{}'.format(__name__))


@dashboard
def home(request):
    hero = Comic.hero(site=request.site)

    if not hero:
        c = Comic(title="Hello World",
                  image_url="http://curtis.lassam.net/comics/cube_drone/misc_assets/mail.png",
                  posted = timezone.now(),
                  published = True,
                  secret_text = "There aren't any comics on this site, yet!")
        c.save()
        hero = Comic.hero(site=request.site)
    permalink = _permalink(request, hero.slug)
    return render(request,
                  "comics/single.html",
                  {'slug': hero.slug,
                   'permalink': permalink,
                   'comic':hero})


@dashboard
def single_by_numerical_order(request, n):
    """ redirect to single by slug """
    if int(n) <= 0:
        raise Http404("There's no Comic 0.")
    comic = get_object_or_404(Comic, order=n)
    return HttpResponseRedirect(reverse(single,
                                kwargs={'comic_slug': comic.slug}))

def _permalink(request, comic_slug):
    return request.build_absolute_uri(reverse(single,
                                              kwargs={'comic_slug':comic_slug}))


@login_required
def preview(request, site_slug, comic_slug):
    comic = get_object_or_404(Comic, site__slug=site_slug, slug=comic_slug)
    return render(request, "comics/single.html", {'preview': True,
                                                  'slug': comic_slug,
                                                  'site_slug': site_slug,
                                                  'comic': comic})


# Archives
# --------------

@dashboard
def single(request, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)
    if comic.hidden:
        raise Http404("This comic has been removed!")
    if timezone.now() < comic.posted:
        raise Http404("This comic hasn't been posted yet!")
    permalink = _permalink(request, comic_slug)
    return render(request, "comics/single.html", {'preview': False,
                                                  'dashboard': {'page_title':comic.title},
                                                  'slug': comic_slug,
                                                  'permalink': permalink,
                                                  'comic': comic})

@dashboard
def archives(request):
    archives = Comic.archives(site=request.site)
    tags = Comic.all_tags(site=request.site)
    return render(request, "comics/archives.html", {'comics': archives,
                                                    'tags': tags})


@dashboard
def tag(request, slug):
    archives = Comic.archives(site=request.site).filter(tags__contains=[slug])
    tags = Comic.all_tags(site=request.site)
    return render(request, "comics/archives.html", {'comics': archives,
                                                    'active_tag': slug,
                                                    'tags': tags})

@dashboard
def search(request):
    try:
        search_term = request.GET['search']
    except KeyError:
        return HttpResponseRedirect(reverse(archives))
    comics = Comic.objects.search(search_term).filter(hidden=False, site=request.site)
    tags = Comic.all_tags(site=request.site)
    return render(request, "comics/archives.html", {'comics':comics,
                                                    'search_term': search_term,
                                                    'tags': tags})


@dashboard
def blog(request):
    archives = Comic.archives(site=request.site)
    blogs = []
    for comic in archives:
        for blog_post in comic.blog_posts:
            blogs.append(blog_post)
    return render(request, "comics/blog.html", {'blogs':blogs})


@dashboard
def manage_redirect(request):
    return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':request.site.slug}))


@login_required
def manage(request, site_slug):
    site = get_object_or_404(SiteOptions, slug=site_slug)
    backlog = Comic.backlog(site=site)
    archives = Comic.archives(site=site)
    hero = Comic.hero(site=site)
    tags = Comic.all_tags(site=site)
    return render(request, "comics/manage.html", {
        'tags': tags,
        'backlog': backlog,
        'archives': archives,
        'site_slug': site_slug,
        'hero': hero})


@login_required
def manage_tag(request, site_slug, slug):
    site = get_object_or_404(SiteOptions, slug=site_slug)
    backlog = Comic.backlog(site=site).filter(tags__contains=[slug])
    archives = Comic.archives(site=site).filter(tags__contains=[slug])
    tags = Comic.all_tags(site=site)
    return render(request, "comics/manage.html", {
        'tags': tags,
        'active_tag': slug,
        'backlog': backlog,
        'site_slug': site_slug,
        'archives': archives})


@login_required
def trash(request, site_slug):
    site = get_object_or_404(SiteOptions, slug=site_slug)
    trash = Comic.trash(site=site)
    return render(request, "comics/manage_trash.html", {
        'trash': trash,
        'site_slug': site_slug,
    })


@login_required
def create(request, site_slug):
    site = get_object_or_404(SiteOptions, slug=site_slug)
    now = datetime.datetime.now()
    if request.method == 'POST':
        form = ComicForm(request.POST)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.site = site
            comic.save()
            messages.add_message(request, messages.SUCCESS, 'Comic Created!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = ComicForm(initial={'posted':now})

    return render(request, 'comics/create.html', {'form': form, 'site_slug':site_slug})


@login_required
def update(request, site_slug, comic_slug):
    site = get_object_or_404(SiteOptions, slug=site_slug)
    comic = get_object_or_404(Comic, slug=comic_slug, site__slug=site_slug)
    print("Updating comic!")
    if request.method == 'POST':
        form = ComicForm(request.POST, instance=comic)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.site = site
            comic.save()
            messages.add_message(request, messages.SUCCESS, 'Comic Updated!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = ComicForm(instance=comic)

    return render(request,
                  'comics/update.html',
                  {'form': form,
                   'site_slug': site_slug,
                   'slug': comic_slug,
                   'comic':comic})


@login_required
def delete(request, site_slug, comic_slug):
    comic = get_object_or_404(Comic, site__slug=site_slug, slug=comic_slug)
    comic.hide()
    log.info("{} deleted".format(comic))
    messages.add_message(request, messages.INFO,
                         "\"{}\" Deleted".format(comic.title))
    return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))


@login_required
def create_blog(request, site_slug, comic_slug):
    comic = get_object_or_404(Comic, site__slug=site_slug, slug=comic_slug)
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.comic = comic
            blog.save()
            messages.add_message(request, messages.SUCCESS, 'Blog Created!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = BlogForm(initial={'comic':comic})

    return render(request, 'comics/create_blog.html', {'form': form, 'site_slug':site_slug, 'comic_slug': comic_slug})


@login_required
def update_blog(request, site_slug, comic_slug, slug):
    blog = get_object_or_404(Blog, comic__site__slug=site_slug, comic__slug=comic_slug, slug=slug)
    print("Blog {} Updated".format(blog))
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Blog Updated!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = BlogForm(instance=blog)

    return render(request, 'comics/update_blog.html', {'form': form, 'site_slug': site_slug, 'comic_slug': comic_slug, 'slug': slug})


@login_required
def delete_blog(request, site_slug, comic_slug, slug):
    blog = get_object_or_404(Blog, comic__site__slug=site_slug, comic__slug=comic_slug, slug=slug)
    blog.hide()
    log.info("{} deleted".format(blog))
    messages.add_message(request, messages.INFO,
                         "\"{}\" Deleted".format(blog.title))
    return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))

@login_required
def create_video(request, site_slug, comic_slug):
    comic = get_object_or_404(Comic, site__slug=site_slug, slug=comic_slug)
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Video Created!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = VideoForm(initial={'comic':comic})

    return render(request, 'comics/create_video.html', {'form': form, 'site_slug':site_slug, 'comic_slug': comic_slug})


@login_required
def update_video(request, site_slug, comic_slug, slug):
    video = get_object_or_404(Video, comic__site__slug=site_slug, comic__slug=comic_slug, slug=slug)
    print("Video {} Updated".format(video))
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Video Updated!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = VideoForm(instance=video)

    return render(request, 'comics/update_video.html', {'form': form, 'site_slug':site_slug, 'comic_slug': comic_slug, 'slug': slug})


@login_required
def delete_video(request, site_slug, comic_slug, slug):
    video = get_object_or_404(Video, comic__site__slug=site_slug, comic__slug=comic_slug, slug=slug)
    video.hide()
    log.info("{} deleted".format(video))
    messages.add_message(request, messages.INFO,
                         "\"{}\" Deleted".format(video.title))
    return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))

@login_required
def create_image(request, site_slug, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug, site__slug=site_slug)
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Image Created!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = ImageForm(initial={'comic':comic})

    return render(request, 'comics/create_image.html', {'form': form, 'site_slug':site_slug, 'comic_slug': comic_slug})


@login_required
def update_image(request, site_slug, comic_slug, slug):
    image = get_object_or_404(Image, comic__site__slug=site_slug, comic__slug=comic_slug, slug=slug)
    print("Image {} Updated".format(image))
    if request.method == 'POST':
        form = ImageForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Image Updated!')
            return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
    else:
        form = ImageForm(instance=image)

    return render(request, 'comics/update_image.html', {'form': form, 'site_slug':site_slug, 'comic_slug': comic_slug, 'slug': slug})


@login_required
def delete_image(request, site_slug, comic_slug, slug):
    image = get_object_or_404(Image, comic__site__slug=site_slug, comic__slug=comic_slug, slug=slug)
    image.hide()
    log.info("{} deleted".format(image))
    messages.add_message(request, messages.INFO,
                         "\"{}\" Deleted".format(image.title))
    return HttpResponseRedirect(reverse(manage, kwargs={'site_slug':site_slug}))
