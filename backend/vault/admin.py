from django.contrib import admin
from .models import VaultEntry, TOTPDevice, fileEntry, RecoverySecret

# Register your models here.

admin.site.register(VaultEntry)
admin.site.register(TOTPDevice)
admin.site.register(fileEntry)
admin.site.register(RecoverySecret)
