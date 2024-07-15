from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
from django_otp.models import Device
import os

User = get_user_model()


def generate_salt():
    return os.urandom(16).hex()


class ClientKeyDerivationSalt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="salt")
    salt = models.CharField(
        max_length=64, default=generate_salt
    )  # Note the absence of parentheses

    def __str__(self):
        return self.user.username


class VaultEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255)
    password = models.CharField(null=False)
    iv = models.CharField(null=False)

    def __str__(self):
        return self.name


class TOTPDevice(Device):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=255, null=False)
