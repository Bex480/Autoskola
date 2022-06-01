from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.admin.serializers.update_user import UpdateSerializer
from api.models.user import PlatformUser
from api.serializers.user import UserSerializer


class UpdateUserView(GenericAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = PlatformUser.objects.filter(id=pk).update(
            **serializer.validated_data,
            username=serializer.validated_data.get("email")
        )

        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)
