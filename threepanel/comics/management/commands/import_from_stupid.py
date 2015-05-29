import datetime
import os
import re
import iso8601
import json

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from slugify import slugify

from comics.models import Comic, Blog, Video, Image

def create_comic(item, posted, comic_url):
    secrettext = ""
    if 'secret-text' in item:
        secrettext = item['secret-text']
    alttext = ""
    if 'alt-text' in item:
        alttext = item['alt-text']

    tags = []
    for category in item['categories']:
        tags.append(slugify(category))

    if 'cube-drone' in tags:
        tags.remove('cube-drone')

    if '-' in item['title']:
        things = [thing.strip(" ") for thing in item['title'].split("-")]
        if "Interlude" in things or "interlude" in things:
            tags.append('interlude')
            things = things[1:]
        try:
            int(things[0])
            things = things[1:]
        except ValueError:
            pass
        item['title'] = " ".join(things)

    c = Comic(title=item['title'],
              posted=posted,
              image_url=comic_url,
              secret_text=secrettext,
              alt_text=alttext,
              promo_text="",
              hidden=not item['visible'],
              published=True,
              tags=tags)
    c.save()
    print("Created {}".format(c))

def create_image(title, image):
    hero = Comic.hero()
    print(hero)

    i = Image(comic=hero,
              title=title,
              image_url=image)
    i.save()
    print("Created {}".format(i))

def create_blog(item):
    hero = Comic.hero()
    content = ""
    if "markdown" in item:
        content = item['markdown']
    elif "content" in item:
        content = item['content']

    b = Blog(comic=hero,
             title=item['title'],
             markdown=content,
             hidden= not item['visible'])
    b.save()
    print("Created {}".format(b))

def create_video(item):
    hero = Comic.hero()

    v = Video(comic=hero,
              title=item['title'],
              youtube_video_code=item['youtube'],
              hidden= not item['visible'])
    v.save()
    print("Created {}".format(v))

def irc2markdown(irc):
    lines = irc.split("\n")
    return("* "+"\n* ".join([line.replace("<"," **").replace(">","**: ")
                         for line in lines]))

def create_irc(item):
    content = ""
    if 'irc' in item:
        content = item['irc']
    elif 'content' in item:
        content = item['content']
    irc = irc2markdown(content)
    item['markdown'] = irc
    create_blog(item)

class Command(BaseCommand):
    help = 'Converts a bunch of data from arglebargle format. '

    def handle(self, *args, **options):
        filename = "index.json"
        with open(filename, "r") as stream:
            js = json.load(stream)
            for item in js:
                content_type = item['content-type']
                posted = iso8601.parse_date(item['created'])
                if not 'visible' in item:
                    item['visible'] = True

                if content_type == 'html':
                    srch = re.search("(?P<url>https?://[^\s\"]+)", item['html'])
                    if srch:
                        comic_url = srch.group("url")
                        create_comic(item, posted, comic_url)
                    else:
                        print("{} has no comic in it".format(item['id']))
                elif content_type == 'comic':
                    comic_url = item['comic']
                    if type(comic_url) is str:
                        create_comic(item, posted, comic_url)
                        pass
                    else:
                        create_comic(item, posted, comic_url[0])
                        if len(comic_url) > 1:
                            other_comics = comic_url[1:]
                            counter = 2
                            for comic in other_comics:
                                create_image(title="Part {}".format(counter),
                                             image=comic)
                                counter += 1
                elif content_type == 'markdown':
                    create_blog(item)
                    pass
                elif content_type == 'youtube':
                    create_video(item)
                    pass
                elif content_type == 'irc':
                    create_irc(item)
                else:
                    print("Can't handle {}".format(content_type))

                print("-----------")

