from rest_framework.views import APIView
from rest_framework.response import Response
from vault import models
from rest_framework_simplejwt.authentication import JWTAuthentication
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class Register(APIView):
    def post(self, request):
        try:
            user = models.User.objects.create(
                username=request.data["username"],
            )
            user.set_password(request.data["password"])
            user.save()
            salt = models.ClientKeyDerivationSalt.objects.create(user=user)
            salt.save()
            return Response({"message": "User created"}, status=200)
        except Exception as e:
            return Response({"message": "User creation failed"}, status=400)


class SaltResponse(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            salt = models.ClientKeyDerivationSalt.objects.get(user=request.user)
            return Response({"salt": salt.salt}, status=200)
        except Exception as e:
            return Response({"message": "Failed to retrieve Salt"}, status=400)


class VaultEntry(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            entry = models.VaultEntry.objects.create(
                user=request.user,
                name=request.data["name"],
                username=request.data["username"],
                password=request.data["password"],
                iv=request.data["iv"],
            )
            entry.save()
            return Response({"message": "Entry created"}, status=200)
        except Exception as e:
            return Response({"message": "Entry creation failed"}, status=400)
