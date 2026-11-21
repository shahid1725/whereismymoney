from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'created_at', 'is_active')
        read_only_fields = ('id', 'created_at', 'is_active')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
