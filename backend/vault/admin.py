from django.contrib import admin
from .models import VaultEntry, TOTPDevice

# Register your models here.

admin.site.register(VaultEntry)
admin.site.register(TOTPDevice)
