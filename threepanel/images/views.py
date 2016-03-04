import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect

from dashboard.views import render

from .models import Image
from .forms import ImageForm


log = logging.getLogger('threepanel.{}'.format(__name__))


def view(request, image_slug):
    image = get_object_or_404(Image, slug=image_slug)
    if not image.processed or image.width <= 1000:
        return redirect(image.image_file.url)
    else:
        return redirect(image.resized_url)


def thumbnail(request, image_slug):
    image = get_object_or_404(Image, slug=image_slug)
    if not image.processed:
        return redirect(image.image_file.url)
    else:
        return redirect(image.thumbnail_url)


def original(request, image_slug):
    image = get_object_or_404(Image, slug=image_slug)
    return redirect(image.image_file.url)

@login_required
def manage(request):
    images = Image.objects.filter(user=request.user).order_by('-created')[:10]
    count = Image.objects.filter(user=request.user).count()
    form = ImageForm()
    return render(request, "images/manage.html", {
        'form': form,
        'images': images,
        'count': count})

def manage_redirect(request):
    return redirect(manage)

@login_required
def archives(request):
    images = Image.objects.filter(user=request.user).order_by('-created')
    form = ImageForm()
    return render(request, "images/archives.html", {
        'form': form,
        'images': images})


@login_required
def create(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            image.process()
            log.info("User {} created image {}:{}x{}".format(request.user, image.slug, image.height, image.width))
            messages.add_message(request, messages.SUCCESS, 'Image created!')
            return redirect(reverse(manage))
    else:
        form = ImageForm()

    return render(request, 'images/create.html', {'form': form})


@login_required
def create_js(request):
    if 'file' in request.FILES:
        request.FILES['image_file'] = request.FILES['file']
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            image.process()
            log.info("User {} created image {}:{}x{}".format(request.user, image.slug, image.height, image.width))
            return HttpResponse(image.slug)
        else:
            if "image_file" in form.errors:
                #errors = " ".join([error['message'] for error in form.errors['image_file']])
                return HttpResponseBadRequest(form.errors['image_file'])
            else:
                return HttpResponseBadRequest("I AM ERROR")
    else:
        form = ImageForm()

    return render(request, 'images/create.html', {'form': form})


@login_required
def trash(request):
    pass
