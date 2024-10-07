from django.contrib import admin
from django.urls import path

from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("token", TokenObtainPairViewWith2FA.as_view(), name="token"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("register", Register.as_view(), name="register"),
    path("salt", SaltResponse.as_view(), name="salt"),
    path("confirm2fa", ConfirmTwoFactor.as_view(), name="2fa"),
    path("vault/add", VaultAdd.as_view(), name="vault-add"),
    path("vault/add-batch", VaultAddBatch.as_view(), name="vault-add-batch"),
    path("vault/retrieve", VaultRetrieve.as_view(), name="vault-retrieve"),
    path("vault/delete", VaultDelete.as_view(), name="vault-delete"),
    path("vault/edit", VaultEdit.as_view(), name="vault-edit"),
    path("vault/files/add", FileAdd.as_view(), name="file-add"),
    path("vault/files/delete", FileDelete.as_view(), name="file-delete"),
    path("recovery", Recovery.as_view(), name="recovery"),
]
