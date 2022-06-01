from rest_framework import serializers
from api.models.user import PlatformUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'verification_token'
        ]

        #x-csrftoken
