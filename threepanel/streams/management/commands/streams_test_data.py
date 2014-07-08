# Python Imports
import string
import datetime

# Django Imports
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.timezone import make_aware, utc

# Local Imports
from random_name import noun, adjective, title, name
from ...models import Account, Stream, Article, Content 

class Command(BaseCommand):
    args = '<no args>'
    help = 'Installs a fake Account hierarchy.'

    def handle(self, *args, **options):
        username = name()
        password = noun()
        email = adjective()+"@"+noun()+".fake"
        self.stdout.write("Creating username: %s, password: %s, email: %s" % 
              (username, password, email))
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            self.stdout.write("FAILED: IntegrityError")

        adj = adjective()
        nn = noun()
        account = Account(user=user,
                          slug=adj+"-"+nn, 
                          title=string.capwords(adj+" "+nn))
        account.save()
        self.stdout.write("Created account %s" % (str(account),))

        comics = Stream(account=account,
                        slug="comics",
                        title="Comics",
                        description="A daily comic about %s %s" % (adj, nn))
        comics.save()

        blog = Stream(account=account,
                        slug="blog",
                        title="Blog",
                        description="My blog!")
        blog.save()
        self.stdout.write("Created stream %s" % (blog,))

        article = Article(stream=blog,
                          status=Article.STATUS.published,
                          datetime=make_aware(datetime.datetime.now(), utc),
                          title="Everything is awesome!")
        article.save()
        self.stdout.write("Created article %s" % (str(article),))
        
        content = Content(article=article,
                          order=0,
                          content_type='markdown',
                          content={
                              'content':'Hi, there.'
                              }
                          )
        content.save()
        self.stdout.write("Created content %s" % (content,))
        
        article = Article(stream=comics,
                          status=Article.STATUS.draft,
                          datetime=make_aware(datetime.datetime.now(), utc),
                          title=name())
        article.save()
        self.stdout.write("Created article %s" % (str(article),))
        
        content = Content(article=article,
                          order=0,
                          content_type='external_image',
                          content={
                              'url': 'http://curtis.lassam.net/comics/cube_drone/82.gif',
                              'alt-tag': 'You are reading this now.'
                              }
                          )
        content.save()
        self.stdout.write("Created content %s" % (str(content),))
        
        content = Content(article=article,
                          order=-1,
                          content_type='markdown',
                          content={
                              'content': 'Hey, this is a blog post written in Markdown',
                              }
                          )
        content.save()
        self.stdout.write("Created content %s" % (str(content),))
        
        article = Article(stream=comics,
                          status=Article.STATUS.published,
                          datetime=make_aware(
                            datetime.datetime.now()-datetime.timedelta(days=1),
                            utc),
                          title=name())
        article.save()
        self.stdout.write("Created article %s" % (str(article),))
        
        content = Content(article=article,
                          order=-1,
                          content_type='markdown',
                          content={
                              'content': 'Hey, this is a different blog post',
                              }
                          )
        content.save()
        self.stdout.write("Created content %s" % (str(content),))
