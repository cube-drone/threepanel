import os
import shutil

from django.test import TestCase
from django.core.files.images import ImageFile
from django.contrib.auth.models import User
from django.conf import settings

from .models import Image

# Create your tests here.

class ImageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testy',
                                             email='testytesterson@sample.org',
                                             password='top_secret')

        with open(settings.BASE_DIR + '/images/test.png', 'rb') as f:
            self.test_image = Image(user=self.user)
            self.test_image.image_file.save('test.png', ImageFile(f))
            self.test_image.save()

        with open(settings.BASE_DIR + '/images/test.jpg', 'rb') as f:
            self.test_image_jpg = Image(user=self.user)
            self.test_image_jpg.image_file.save('test.jpg', ImageFile(f))
            self.test_image_jpg.save()

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT + '/user_testy')
        pass

    def test_image_creation(self):
        self.assertEqual(self.test_image.width, 1000)
        self.assertEqual(self.test_image.height, 563)
        self.assertEqual(self.test_image_jpg.width, 745)
        self.assertEqual(self.test_image_jpg.height, 335)

    def test_thumbnail(self):
        self.test_image.thumbnail()
        self.assertTrue(os.path.exists(self.test_image.thumbnail_filename))

    def test_jpg_thumbnail(self):
        self.test_image_jpg.thumbnail()
        self.assertTrue(os.path.exists(self.test_image_jpg.thumbnail_filename))

    def test_resized(self):
        self.test_image.resize()
        self.assertTrue(os.path.exists(self.test_image.resized_filename))

    def test_jpg_resized(self):
        self.test_image_jpg.resize()
        self.assertTrue(os.path.exists(self.test_image_jpg.resized_filename))
