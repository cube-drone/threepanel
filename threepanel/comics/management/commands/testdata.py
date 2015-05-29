import datetime
import random

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from slugify import slugify

from comics.models import Comic, Blog, Video, Image
from publish.models import EmailSubscriber
from django.contrib.auth.models import User
import random_name


def random_comic(posted):
    words = random_name.special_thing()

    c = Comic(title=words,
              image_url="http://curtis.lassam.net/comics/cube_drone/{}.gif".format(random.choice(range(0, 140))),
              promo_text= "Promo text for {}".format(words)[:79],
              posted=posted,
              secret_text = "Secret text for {}".format(words),
              alt_text = "Alt text for {}".format(words),
              tags = [random_name.thing(), random_name.adjective(), random_name.noun()])
    if random.choice([False, False, False, True]):
        c.title = "Hidden {}".format(c.title)
        c.hidden = True
    c.save()
    print("Creating {}".format(c))
    return c

def create_comics():
    comics = []
    for i in range(0,50):
        n_days_ago = timezone.now() - datetime.timedelta(days=i)
        comics.append(random_comic(n_days_ago))
    for i in range(0,4):
        n_days_ahead = timezone.now() + datetime.timedelta(days=i)
        comics.append(random_comic(n_days_ahead))
    return comics

def create_blogs(comics):
    for comic in comics:
        b = Blog(comic=comic,
                 title=random_name.thing().title(),
                 markdown=random_name.markdown())
        b.save()
        print("Creating {}".format(b))

def create_videos(comics):
    for comic in comics:
        vcode = random.choice(['VYvMOf3hsGA',
            'uAOQQogTiaI',
            'oiMZa8flyYY',
            'Rb4lgOiHBZo',
            'RrG4JnrN5GA',
            'eA0RF5ciJXE',
            'Bifmj1O3D24',
            'YLO7tCdBVrA'
        ])
        v = Video(comic=comic,
                  title=random_name.thing().title(),
                  youtube_video_code=vcode)
        v.save()
        print("Creating {}".format(v))

def create_images(comics):
    for comic in comics:
        i = Image(comic=comic,
                  title=random_name.thing().title(),
                  image_url="http://curtis.lassam.net/comics/cube_drone/{}.gif".format(random.choice(range(0, 140))),
                  secret_text=random_name.thing(),
                  alt_text=random_name.adjective())
        i.save()
        print("Creating {}".format(i))

def create_subscribers():
    for i in range(0, 15):
        n_hours_ago = timezone.now() - datetime.timedelta(hours=12*i)
        email = "{}@sample.org".format(slugify(random_name.proper_name()))
        verified = i % 2 == 0
        e = EmailSubscriber(email = email,
                            verified = verified)
        e.save()
        e.last_email_sent = n_hours_ago
        e.created = n_hours_ago
        e.save()
        print("Creating {}".format(e))

class Command(BaseCommand):
    help = 'Writes test data to the database'

    def handle(self, *args, **options):
        print("Creating superuser: classam/butts")
        user = User.objects.create_superuser('classam', 'curtis@lassam.net', 'butts')
        user.save()

        comics = create_comics()
        create_blogs(comics)
        create_videos(comics)
        create_images(comics)
        create_subscribers()

