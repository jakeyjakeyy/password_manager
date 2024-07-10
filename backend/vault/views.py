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
            user = models.User.objects.create_user(
                username=request.data["username"],
                password=request.data["password"],
            )
            user.save()
            return Response({"message": "User created"}, status=200)
        except Exception as e:
            return Response({"message": "User creation failed"}, status=400)


class SaltResponse(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            salt = models.User.objects.get(username=request.user)
            password_components = salt.password.split("$")
            return Response({"salt": password_components[2]}, status=200)
        except Exception as e:
            return Response({"message": "Failed to retrieve Salt"}, status=400)
