from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import os

class Appuser(AbstractUser):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("Users", self.username, instance)
        return None

    ROLES  = (
        ('admin', 'admin'),
        ('médico', 'médico'),
        ('investigador', 'investigador'),
    )

    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=100, choices=ROLES ,)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    userid = models.AutoField( primary_key=True)  # Field name made lowercase.
    last_login = models.DateTimeField( blank=True, null=True)
    useremail = models.CharField( unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField( max_length=100, blank=True, null=True)  # Field name made lowercase.
    savedate = models.DateTimeField( auto_now_add=True, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.email
