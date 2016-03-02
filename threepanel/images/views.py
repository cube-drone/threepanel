import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect

from dashboard.views import render

from .models import Image
from .forms import ImageForm


log = logging.getLogger('threepanel.{}'.format(__name__))


def view(request, image_slug):
    image = get_object_or_404(Image, slug=image_slug)
    if not image.processed:
        return redirect(image.image_file.url)
    else:
        return redirect(image.resized_url, permanent=True)


def thumbnail(request, image_slug):
    image = get_object_or_404(Image, slug=image_slug)
    if not image.processed:
        return redirect(image.image_file.url)
    else:
        return redirect(image.thumbnail_url, permanent=True)


def original(request, image_slug):
    image = get_object_or_404(Image, slug=image_slug)
    return redirect(image.image_file.url)


@login_required
def manage(request):
    print(request.user)
    images = Image.objects.filter(user=request.user)
    return render(request, "images/manage.html", {
        'images': images})


@login_required
def create(request):
    print(request.user)
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
def trash(request):
    pass
