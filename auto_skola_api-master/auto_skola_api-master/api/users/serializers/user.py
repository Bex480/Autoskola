from rest_framework import serializers
from api.models.user import PlatformUser


class CurrentUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = [
            'first_name',
            'last_name',
            'password'
            ]
