from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.serializers.user import UserSerializer
from api.users.serializers.user import CurrentUserUpdateSerializer


class CurrentUserView(GenericAPIView):
    serializer_class = CurrentUserUpdateSerializer
    permission_classes = []

    def get(self, request):
        current_user = request.user
        return Response(data=UserSerializer(current_user).data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = CurrentUserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_user = request.user

        current_user.set_password(serializer.validated_data.pop("password"))
        current_user.first_name = serializer.validated_data.pop("first_name")
        current_user.last_name = serializer.validated_data.pop("last_name")

        current_user.save()

        return Response(data=UserSerializer(current_user).data, status=status.HTTP_200_OK)


