from django.core.management.base import BaseCommand
from app.views import cache_pop_tags
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cache_pop_tags()