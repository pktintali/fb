import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin2').exists():
            User.objects.create_superuser('admin2',
                                          'admin2@domain.com',
                                          '@@4444@@')
