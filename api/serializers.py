from rest_framework import serializers

from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'name',
            'email',
            'password',
            'created_at',
            'updated_at'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile

        fields = [
            'id',
            'full_name',
            'bio',
            'phone_number',
            'address',
            'user',
            'created_at',
            'updated_at'
        ]