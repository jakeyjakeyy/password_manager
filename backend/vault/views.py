from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from vault import models
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from dotenv import load_dotenv
import logging
import pyotp
import time

load_dotenv()

logger = logging.getLogger(__name__)


class Register(APIView):
    def post(self, request):
        try:
            user, created = models.User.objects.get_or_create(
                username=request.data["username"],
            )
            if not created:
                return Response({"error": "User already exists"}, status=409)
            user.set_password(request.data["password"])
            user.save()
            salt = models.ClientKeyDerivationSalt.objects.create(user=user)
            salt.save()

            # 2FA registration
            totpDevice = models.TOTPDevice.objects.create(
                user=user, secret=pyotp.random_base32()
            )
            # Generate QR code URI
            totp = pyotp.TOTP(totpDevice.secret)
            uri = totp.provisioning_uri(name=user.username, issuer_name="Vault")

            return Response(
                {"message": "User created", "uri": uri, "salt": salt.salt}, status=200
            )
        except Exception as e:
            return Response({"error": "User creation failed"}, status=400)


class ConfirmTwoFactor(APIView):
    def post(self, request):
        try:
            user = request.data["user"]
            user = models.User.objects.get(username=user)
            totp = models.TOTPDevice.objects.get(user=user)
            totp.confirmed = True
            totp.save()
            return Response({"message": "2FA confirmed"}, status=200)
        except Exception as e:
            return Response({"message": "Failed to confirm 2FA"}, status=400)


class Recovery(APIView):
    throttle_scope = "strict"

    def post(self, request):
        try:
            user = models.User.objects.get(username=request.data["username"])
            if not user:
                return Response({"message": "Unauthorized"}, status=401)

            if request.data["verify"]:
                provided_secret = request.data["secret"]
                recovery_secret = models.RecoverySecret.objects.get(user=user)
                if recovery_secret.attempts >= 3:
                    if time.time() - recovery_secret.last_attempt.timestamp() < 60 * 60:
                        return Response(
                            {"message": "Too many attempts. Try again later"},
                            status=429,
                        )
                    recovery_secret.attempts = 0
                is_valid = recovery_secret.check_secret(provided_secret)
                password_bytes = bytes.fromhex(recovery_secret.password)
                password = {
                    str(index): byte for index, byte in enumerate(password_bytes)
                }
                iv_bytes = bytes.fromhex(recovery_secret.iv)
                iv = {str(index): byte for index, byte in enumerate(iv_bytes)}
                if is_valid:
                    salt = models.ClientKeyDerivationSalt.objects.get(user=user)
                    return Response(
                        {
                            "password": password,
                            "iv": iv,
                            "salt": salt.salt,
                        },
                        status=200,
                    )
                else:
                    recovery_secret.attempts += 1
                    recovery_secret.last_attempt = time.strftime("%Y-%m-%d %H:%M:%S")
                    recovery_secret.save()
                    return Response({"message": "Unauthorized"}, status=401)
            else:
                raw_secret = request.data["secret"]
                recovery_secret, created = models.RecoverySecret.objects.get_or_create(
                    user=user
                )
                recovery_secret.set_secret(raw_secret)
                password_bytes = ToBytes(request.data["password"])
                iv_bytes = ToBytes(request.data["iv"])
                recovery_secret.iv = iv_bytes.hex()
                recovery_secret.password = password_bytes.hex()
                recovery_secret.save()
                return Response({"message": "Recovery secret set"}, status=200)
        except Exception as e:
            logger.error(f"Recovery failed: {str(e)}")
            return Response({"message": "Failed to set recovery secret"}, status=400)


class ResetPassword(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            user = request.user
            oldPassword = request.data["oldPassword"]
            newPassword = request.data["newPassword"]
            if not user.check_password(oldPassword):
                return Response({"message": "Unauthorized"}, status=401)

            user.set_password(newPassword)
            user.save()
            return Response({"message": "Password reset"}, status=200)
        except Exception as e:
            logger.error(f"Password reset failed: {str(e)}")
            return Response({"message": "Failed to reset password"}, status=400)


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
            password_bytes = ToBytes(request.data["password"])
            iv_bytes = ToBytes(request.data["iv"])
            if models.VaultEntry.objects.filter(
                user=request.user, name=request.data["name"]
            ).exists():
                return Response(
                    {"message": "Entry with the same name already exists"}, status=400
                )
            entry = models.VaultEntry.objects.create(
                user=request.user,
                name=request.data["name"],
                username=request.data["username"],
                password=password_bytes.hex(),
                iv=iv_bytes.hex(),
            )
            entry.save()
            return Response({"message": "Entry created", "id": entry.id}, status=200)
        except Exception as e:
            logger.error(f"Entry creation failed: {str(e)}")
            return Response({"message": "Entry creation failed"}, status=400)


class VaultAddBatch(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        errors = []
        entries = request.data["entries"]
        for entry in entries:
            try:
                password_bytes = ToBytes(entry["password"])
                iv_bytes = ToBytes(entry["iv"])
                if models.VaultEntry.objects.filter(
                    user=request.user, name=entry["name"]
                ).exists():
                    errors.append(
                        {
                            "name": entry["name"],
                            "message": "Entry with the same name already exists",
                        }
                    )
                    continue
                entry = models.VaultEntry.objects.create(
                    user=request.user,
                    name=entry["name"],
                    username=entry["username"],
                    password=password_bytes.hex(),
                    iv=iv_bytes.hex(),
                )
                entry.save()
            except Exception as e:
                errors.append({"name": entry["name"], "message": str(e)})
        if len(errors) > 0:
            return Response(
                {"message": "Failed to create entries", "errors": errors}, status=400
            )
        return Response({"message": "Success"}, status=200)


class VaultDelete(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            entry = models.VaultEntry.objects.get(id=request.data["id"])
            if entry.user != request.user:
                return Response({"message": "Unauthorized"}, status=401)
            entry.delete()
            return Response({"message": "Entry deleted"}, status=200)
        except Exception as e:
            logger.error(f"Failed to delete entry: {str(e)}")
            return Response({"message": "Failed to delete entry"}, status=400)


class VaultEdit(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            entry = models.VaultEntry.objects.get(id=request.data["id"])
            if entry.user != request.user:
                return Response({"message": "Unauthorized"}, status=401)
            password_bytes = ToBytes(request.data["password"])
            iv_bytes = ToBytes(request.data["iv"])
            entry.name = request.data["name"]
            entry.username = request.data["username"]
            entry.password = password_bytes.hex()
            entry.iv = iv_bytes.hex()
            entry.save()
            return Response({"message": "Entry edited"}, status=200)
        except Exception as e:
            return Response({"message": "Failed to edit entry"}, status=400)


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

                files = []
                for file in entry.files.all():
                    fileBytes = bytes.fromhex(file.file)
                    ivBytes = bytes.fromhex(file.iv)
                    files.append(
                        {
                            "name": file.name,
                            "iv": {
                                str(index): byte for index, byte in enumerate(ivBytes)
                            },
                            "file": {
                                str(index): byte for index, byte in enumerate(fileBytes)
                            },
                            "id": file.id,
                        }
                    )
                response.append(
                    {
                        "name": entry.name,
                        "username": entry.username,
                        "password": password,
                        "iv": iv,
                        "id": entry.id,
                        "files": files,
                    }
                )
            return Response(response, status=200)
        except Exception as e:
            return Response({"message": "Failed to retrieve entries"}, status=400)


# Extend the default TokenObtainPairSerializer to include 2FA
class TokenObtainPairSerializerWith2FA(TokenObtainPairSerializer):
    default_error_messages = {
        "no_2fa": "2FA is not set up for this user. Account will be deleted.",
        "no_recovery": "Recovery secret is not set up for this user. Account will be deleted.",
        "invalid_2fa": "Invalid 2FA token.",
    }

    def validate(self, attrs):
        # Standard validation to check user credentials
        data = super().validate(attrs)

        user = self.user

        recovery = models.RecoverySecret.objects.filter(user=user).exists()
        if not recovery:
            user.delete()
            raise serializers.ValidationError(
                self.default_error_messages["no_recovery"]
            )
        topt = models.TOTPDevice.objects.get(user=user)
        if not topt.confirmed:
            user.delete()
            raise serializers.ValidationError(self.default_error_messages["no_2fa"])

        # debug: Returning here to skip 2FA check
        return data

        # Get the 2FA token from the request
        two_fa_token = self.context["request"].data.get("twoFA", None)
        if two_fa_token is None:
            raise serializers.ValidationError(
                self.default_error_messages["invalid_2fa"]
            )
        # Verify the 2FA token
        totp = pyotp.TOTP(user.totpdevice.secret)
        if not totp.verify(two_fa_token):
            raise serializers.ValidationError(
                self.default_error_messages["invalid_2fa"]
            )

        return data


class TokenObtainPairViewWith2FA(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializerWith2FA


# class VaultImport(APIView):
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):


def ToBytes(input):
    return bytes([input[str(k)] for k in sorted(input.keys(), key=int)])


class FileAdd(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            entry = models.VaultEntry.objects.get(id=request.data["id"])
            file = request.data["file"]
            fileBytes = ToBytes(file)
            name = request.data["name"]
            iv = request.data["iv"]
            ivBytes = ToBytes(iv)
            if entry.user != request.user:
                return Response({"message": "Unauthorized"}, status=401)
            # check file extension
            if not name.endswith((".txt", ".csv", ".json", ".pdf", ".zip")):
                return Response({"message": "Invalid file type"}, status=422)
            # make sure fize size below 5MB
            if len(fileBytes) > 5 * 1024 * 1024:
                return Response({"message": "Content Too Large"}, status=413)
            file = models.fileEntry.objects.create(
                VaultEntry=entry,
                file=fileBytes.hex(),
                name=request.data["name"],
                iv=ivBytes.hex(),
            )
            file.save()
            return Response({"message": "File uploaded", "id": file.id}, status=200)
        except Exception as e:
            return Response({"message": "Failed to upload file"}, status=400)


class FileDelete(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            file = models.fileEntry.objects.get(id=request.data["id"])
            if file.VaultEntry.user != request.user:
                return Response({"message": "Unauthorized"}, status=401)
            file.delete()
            return Response({"message": "File deleted"}, status=200)
        except Exception as e:
            return Response({"message": "Failed to delete file"}, status=400)


class VaultEditBatch(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            entries = request.data["entries"]
            errors = []
            for editedEntry in entries:
                try:
                    entry = models.VaultEntry.objects.get(id=editedEntry["id"])
                    if entry.user != request.user:
                        errors.append(
                            {
                                "id": editedEntry["id"],
                                "message": "Unauthorized",
                            }
                        )
                        continue
                    password_bytes = ToBytes(editedEntry["password"])
                    iv_bytes = ToBytes(editedEntry["iv"])
                    entry.name = editedEntry["name"]
                    entry.username = editedEntry["username"]
                    entry.password = password_bytes.hex()
                    entry.iv = iv_bytes.hex()
                    entry.save()

                    for file in editedEntry["files"]:
                        db_file = models.fileEntry.objects.get(id=file["id"])
                        db_file.file = ToBytes(file["file"]).hex()
                        db_file.name = file["name"]
                        db_file.iv = ToBytes(file["iv"]).hex()
                        db_file.save()

                except Exception as e:
                    errors.append({"id": entry["id"], "message": str(e)})
            if len(errors) > 0:
                return Response(
                    {"message": "Failed to edit entries", "errors": errors}, status=400
                )
            return Response({"message": "Success"}, status=200)
        except Exception as e:
            logger.error(f"Failed to edit entries: {str(e)}")
            return Response({"message": "Failed to edit entries"}, status=400)
