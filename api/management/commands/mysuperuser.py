import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='pktintali').exists():
            User.objects.create_superuser('pktintali',
                                          'pktintali@gmail.com',
                                          '@@4444@@')
