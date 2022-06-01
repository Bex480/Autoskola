from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models.user import PlatformUser
from api.serializers.user import UserSerializer
from api.serializers.registration import AccountActivateSerializer


class ActivateAccountView(GenericAPIView):
    permission_classes = []

    def post(self, request, token: str):
        serializer = AccountActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = PlatformUser.objects.filter(verification_token=token).first()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data.pop("password"))
        user.verification_token = None
        user.is_active = True
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


#
# (1) Admin Se loguje
# (2) Admin doda account
# (2.1) Aktivacijski link se salje korisniku na mejl/broj
# (3) User bira password
# (4) User salje password na dati aktivacijski link
#   [1] Pasword je postavljan, racun je aktivran
#   [2] Link invalidan
#   [3] Password Invalidan
