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


class VaultAdd(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            password_bytes = bytes(
                [
                    request.data["password"][str(k)]
                    for k in sorted(request.data["password"].keys(), key=int)
                ]
            )
            iv_bytes = bytes(
                [
                    request.data["iv"][str(k)]
                    for k in sorted(request.data["iv"].keys(), key=int)
                ]
            )
            logger.info(password_bytes.hex())
            logger.info(iv_bytes.hex())
            entry = models.VaultEntry.objects.create(
                user=request.user,
                name=request.data["name"],
                username=request.data["username"],
                password=password_bytes.hex(),
                iv=iv_bytes.hex(),
            )
            logger.info("entry created")
            entry.save()
            return Response({"message": "Entry created"}, status=200)
        except Exception as e:
            logger.error(f"Entry creation failed: {str(e)}")
            return Response({"message": "Entry creation failed"}, status=400)


class VaultRetrieve(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            entries = models.VaultEntry.objects.filter(user=request.user)
            response = []
            for entry in entries:
                password_bytes = bytes.fromhex(entry.password)
                password = {
                    str(index): byte for index, byte in enumerate(password_bytes)
                }

                iv_bytes = bytes.fromhex(entry.iv)
                iv = {str(index): byte for index, byte in enumerate(iv_bytes)}
                response.append(
                    {
                        "name": entry.name,
                        "username": entry.username,
                        "password": password,
                        "iv": iv,
                    }
                )
            return Response(response, status=200)
        except Exception as e:
            return Response({"message": "Failed to retrieve entries"}, status=400)
