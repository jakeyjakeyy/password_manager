from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class ClientKeyDerivationSalt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salt = models.CharField(max_length=64, default=os.urandom(16).hex())

    def __str__(self):
        return self.user.username


class VaultEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    iv = models.CharField(max_length=255)

    def __str__(self):
        return self.name
