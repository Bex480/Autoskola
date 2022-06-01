from rest_framework import serializers


class AccountActivateSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
