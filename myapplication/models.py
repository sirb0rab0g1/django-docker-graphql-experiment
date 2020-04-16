from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from core.upload_path import get_images_upload_path, get_events_upload_path, get_images_path, handle_uploaded_file
from .constants import (
    ROLE_CHOICES
)


class BasicInformation(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=get_images_upload_path, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, choices=ROLE_CHOICES, default='')
    birth_date = models.CharField(max_length=10, blank=True, default='')
    gender = models.CharField(max_length=10, blank=True, default='')
    nationality = models.CharField(max_length=40, blank=True, default='')
    phone_number = models.CharField(max_length=30, blank=True, default='')
    status = models.CharField(max_length=10, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')
    creation_date = models.DateTimeField('user creation', auto_now_add=True, null=True, blank=True)


class Events(models.Model):
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=get_events_upload_path, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=400)
    link = models.CharField(max_length=400, blank=True, null=True)
    creation_date = models.DateTimeField('date created', auto_now_add=True, null=True, blank=True)
