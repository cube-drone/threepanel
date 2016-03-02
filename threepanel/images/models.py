import logging
import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.utils import timezone

from PIL import Image as PIL_Image
from autoslug import AutoSlugField
from slugify import slugify as slugify_wont_serialize

from random_name import int_to_silly_slug


log = logging.getLogger('threepanel.{}'.format(__name__))


def slugify(s):
    return slugify_wont_serialize(s)


def user_directory_path(instance, filename):
    """
    This is where image files will be uploaded to.
    """
    return 'user_{0}/{1}-{2}'.format(instance.user.username, instance.slug, filename)


def silly_slug(instance):
    return int_to_silly_slug(hash(instance.image_file.url))


class Image(models.Model):
    """
    An image file.
    We want to take this image and convert it into a thumbnail,
    a comic-appropriate sized image, and crush both of those using optipng.

    Optipng takes 6 seconds, so it MUST happen as a background task.

    """
    user = models.ForeignKey(User, related_name="images")

    slug = AutoSlugField(populate_from=silly_slug,
                         unique=True,
                         db_index=True,
                         slugify=slugify)

    image_file = models.ImageField(upload_to=user_directory_path,
                                   height_field='height',
                                   width_field='width',
                                   max_length=100)

    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    processed = models.BooleanField(default=False)

    created = models.DateTimeField()

    def save(self):
        if not self.id:
            self.created = timezone.now()
        super().save()

    @property
    def filename(self):
        return os.path.join(settings.MEDIA_ROOT, self.image_file.name)

    @property
    def thumbnail_filename(self):
        filename, ext = os.path.splitext(self.filename)
        return filename + ".thumbnail" + ext

    @property
    def thumbnail_url(self):
        filename, ext = os.path.splitext(self.image_file.url)
        return filename + ".thumbnail" + ext

    @property
    def resized_filename(self):
        filename, ext = os.path.splitext(self.filename)
        return filename + ".resized" + ext

    @property
    def resized_url(self):
        filename, ext = os.path.splitext(self.image_file.url)
        return filename + ".resized" + ext

    def thumbnail(self):
        """
        Convert the file into a thumbnail.
        """
        thumbnail_size = (settings.THUMBNAIL_MAX_WIDTH_PX, settings.THUMBNAIL_MAX_HEIGHT_PX)
        try:
            im = PIL_Image.open(self.filename)
            im.thumbnail(thumbnail_size, PIL_Image.ANTIALIAS)
            im.save(self.thumbnail_filename)
        except IOError:
            log.warning("Cannot create thumbnail for {}".format(self.filename))

    def resize(self):
        """
        Resize the file.
        """
        thumbnail_size = (settings.COMIC_MAX_WIDTH_PX, 10000)
        try:
            im = PIL_Image.open(self.filename)
            im.thumbnail(thumbnail_size, PIL_Image.ANTIALIAS)
            im.save(self.resized_filename)
            print(self.resized_filename)
        except IOError:
            log.warning("Cannot create resized for {}".format(self.filename))
            print("Cannot create resized for {}".format(self.filename))

    def process(self):
        """
        Convert the file into a thumbnail, as well as a
        comic resized to be no wider than 1000px.
        """
        self.thumbnail()
        self.resize()
        self.processed = True
        self.save()
