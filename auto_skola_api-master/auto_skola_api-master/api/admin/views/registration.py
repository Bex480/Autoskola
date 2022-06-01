from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models.user import PlatformUser
from api.serializers.user import UserSerializer
from api.utils.error_handler import WrapperException
from api.utils.errors import LOGIN_IS_BLOCKED, ACCOUNT_DISABLED, INVALID_CREDENTIALS, EMAIL_NOT_VERIFIED
from api.admin.serializers.registration import RegisterSerializer


class CreateUserView(GenericAPIView):
    serializer_class = RegisterSerializer
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = PlatformUser.objects.create_user(
            **serializer.validated_data,
            username=serializer.validated_data.get("email")
        )

        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)
