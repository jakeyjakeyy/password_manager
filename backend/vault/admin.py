from django.contrib import admin
from .models import VaultEntry, TOTPDevice, fileEntry

# Register your models here.

admin.site.register(VaultEntry)
admin.site.register(TOTPDevice)
admin.site.register(fileEntry)
