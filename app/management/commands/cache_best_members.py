from django.core.management.base import BaseCommand
from app.views import cache_best_members
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cache_best_members()