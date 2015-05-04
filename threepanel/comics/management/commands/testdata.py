import datetime
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError
from comics.models import Comic, Blog
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Writes test data to the database'

    def handle(self, *args, **options):
        print("Creating superuser: classam/butts")
        user = User.objects.create_superuser('classam', 'curtis@lassam.net', 'butts')
        user.save()
        comics = []
        for i in range(0,10):
            n_days_ago = timezone.now() - datetime.timedelta(hours=24*(10-i))
            c = Comic(title="Comic {}".format(i),
                      posted=n_days_ago,
                      image_url = "http://curtis.lassam.net/comics/cube_drone/140.gif",
                      promo_text = "BWAAAAAAMP",
                      secret_text = "BWAAAMP is a great sound effect.",
                      alt_text = "*fweep* Cube Drone: Oh, it's an incoming tweet! | *do bweep* I must have an e-mail! | *BWAAAAMP* And that's JIRA")
            if i%4 == 0:
                c.title = c.title + " Hidden"
                c.hidden = True
            c.save()
            print("Creating {}".format(c))
            comics.append(c)
        for i in range(0,10):
            n_days_ago = timezone.now() + datetime.timedelta(hours=24*(10+i))
            c = Comic(title="Comic {}".format(10+i),
                      posted=n_days_ago,
                      image_url = "http://curtis.lassam.net/comics/cube_drone/141.gif",
                      promo_text = "In a lot of ways, coding is like magic.",
                      secret_text = "secret text",
                      alt_text = """A mage stands atop a mountain, holding a staff dramatically to the sky. It fizzles. 'Dammit'.| The mage in his workshop. 'Damn, the documentation says virgin blood, but the staff's API says my blood.'| 'I guess the mad wizard Azabale was not so popular with the ladies.'"""
                      )
            if i%4 == 0:
                c.title = c.title + " Hidden"
                c.hidden = True
            c.save()
            print("Creating {}".format(c))
            comics.append(c)

        for comic in comics:
            b = Blog(comic=comic,
                     title="Blog Post A",
                     markdown="""
An h1 header
============

Paragraphs are separated by a blank line.

2nd paragraph. *Italic*, **bold**, and `monospace`. Itemized lists
look like:

  * this one
  * that one
  * the other one

Note that --- not considering the asterisk --- the actual text
content starts at 4-columns in.

> Block quotes are
> written like so.
>
> They can span multiple paragraphs,
> if you like.

Use 3 dashes for an em-dash. Use 2 dashes for ranges (ex., "it's all
in chapters 12--14"). Three dots ... will be converted to an ellipsis.
Unicode is supported.
                     """)
            b.save()
            print("Creating {}".format(b))
