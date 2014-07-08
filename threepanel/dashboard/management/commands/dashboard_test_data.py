from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from random_name import noun, adjective, title
from django.db import IntegrityError

class Command(BaseCommand):
    args = '<no args>'
    help = 'Installs 10 fake users.'

    def handle(self, *args, **options):
        for i in range(0, 10):
            username = adjective()+"-"+title()+"-"+noun()
            password = adjective()+"-"+noun()
            email = adjective()+"@"+noun()+".fake"
            self.stdout.write("Creating username: %s, password: %s, email: %s" % 
                  (username, password, email))
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                self.stdout.write("FAILED: IntegrityError")
