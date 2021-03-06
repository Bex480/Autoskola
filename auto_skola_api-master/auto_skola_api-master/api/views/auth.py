import logging
import uuid

from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.core.cache import cache

from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from api.models.user import PlatformUser
from api.serializers.user import UserSerializer
from api.utils.error_handler import WrapperException
from api.utils.errors import (
    VERIFICATION_TOKEN_INVALID,
    USER_BY_TOKEN_MISSING,
    EMAIL_NOT_VERIFIED,
    LOGIN_IS_BLOCKED,
    INVALID_CREDENTIALS, ACCOUNT_DISABLED
)
from api.serializers.auth import AuthSerializer


class AuthenticationView(GenericAPIView):
    serializer_class = AuthSerializer
    permission_classes = []

    def post(self, request):
        logout(request)

        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=serializer.validated_data.get("email"), **serializer.validated_data)
        print(user)
        if not user:
            user_with_email = PlatformUser.objects.filter(email=serializer.validated_data.get("email")).first()
            if user_with_email:
                if user_with_email.is_login_blocked:
                    raise WrapperException(LOGIN_IS_BLOCKED)

                if user_with_email.is_disabled:
                    raise WrapperException(ACCOUNT_DISABLED)
            raise WrapperException(INVALID_CREDENTIALS)

        user = PlatformUser.objects.filter(id=user.id).first()
        if not user.is_active:
            raise WrapperException(EMAIL_NOT_VERIFIED)
        if user.is_login_blocked:
            raise WrapperException(LOGIN_IS_BLOCKED)

        login(request, user)

        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
