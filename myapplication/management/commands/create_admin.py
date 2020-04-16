from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from myapplication.models import BasicInformation

User = get_user_model()


def admin_creation():
    if User.objects.filter(username='admin').exists():
        return
    else:
        user = User.objects.create(
            username='admin',
            first_name='admin',
            last_name='admin',
            email='superadmin@superadmin.superadmin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
            date_joined=timezone.now()
        )
        user.set_password('Pasmo.123')
        user.save()
        BasicInformation.objects.create(user=user, role='admin')
        print(f'user created')

class Command(BaseCommand):
    def handle(self, **options):
        admin_creation()
