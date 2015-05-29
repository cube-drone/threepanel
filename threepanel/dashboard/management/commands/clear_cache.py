from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clears the cache'

    def handle(self, *args, **options):
        print("Clearing cache!")
        cache.clear()

